"""
Motor RAG para chatbot-zapopan
Carga y busca en datasets JSONL normativos
"""

import json
import re
from typing import List, Dict, Any, Optional
import pandas as pd
from datetime import datetime

class RAGEngine:
    """Motor de Retrieval-Augmented Generation para normativa Zapopan"""
    
    def __init__(self, dataset_paths: List[str] = None):
        """Inicializar motor RAG con datasets"""
        self.datasets = []
        self.all_chunks = []
        
        # Paths por defecto
        if dataset_paths is None:
            dataset_paths = [
                "001_dataset_rag_combinado.jsonl",
                "002_dataset_rag_combinado.jsonl", 
                "003_dataset_rag_combinado.jsonl"
            ]
        
        self.dataset_paths = dataset_paths
        self.load_datasets()
        
    def load_datasets(self):
        """Cargar todos los datasets JSONL"""
        print(f"📚 Cargando {len(self.dataset_paths)} datasets RAG...")
        
        for path in self.dataset_paths:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    chunks = [json.loads(line) for line in f]
                    self.datasets.append({
                        'path': path,
                        'chunks': chunks,
                        'count': len(chunks)
                    })
                    self.all_chunks.extend(chunks)
                    print(f"  ✅ {path}: {len(chunks)} chunks cargados")
            except Exception as e:
                print(f"  ❌ Error cargando {path}: {e}")
        
        print(f"📊 Total chunks cargados: {len(self.all_chunks)}")
    
    def semantic_search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Búsqueda semántica simple basada en palabras clave
        (En producción, usar embeddings + vector DB)
        """
        query_lower = query.lower()
        
        # Palabras clave normativas comunes
        norm_keywords = [
            'artículo', 'art', 'fracción', 'frac', 'numeral', 'reglamento',
            'código', 'ley', 'norma', 'disposición', 'permiso', 'licencia',
            'infracción', 'sanción', 'competencia', 'facultad', 'atribución'
        ]
        
        # Términos específicos de Zapopan
        zapopan_terms = [
            'zapopan', 'jalisco', 'municipal', 'ayuntamiento', 'inspección',
            'vigilancia', 'comercio', 'construcción', 'medio ambiente',
            'ruido', 'residuos', 'anuncios', 'publicidad', 'obra', 'giro'
        ]
        
        scored_chunks = []
        
        for chunk in self.all_chunks:
            score = 0
            
            # Texto del chunk
            chunk_text = chunk.get('text', '').lower()
            chunk_citation = chunk.get('citation', '').lower()
            
            # 1. Coincidencia exacta en palabras clave normativas
            for keyword in norm_keywords:
                if keyword in query_lower and keyword in chunk_text:
                    score += 2
            
            # 2. Coincidencia en términos de Zapopan
            for term in zapopan_terms:
                if term in query_lower and term in chunk_text:
                    score += 1.5
            
            # 3. Coincidencia de palabras en el texto
            query_words = set(query_lower.split())
            chunk_words = set(chunk_text.split())
            common_words = query_words.intersection(chunk_words)
            score += len(common_words) * 0.1
            
            # 4. Priorizar artículos sobre contenido general
            if chunk.get('unit_type') == 'article':
                score += 1
            
            # 5. Priorizar documentos relevantes por colección
            collection = chunk.get('collection', '').lower()
            if 'construcción' in query_lower and 'construcción' in collection:
                score += 1
            if 'comercio' in query_lower and 'comercio' in collection:
                score += 1
            if 'medio ambiente' in query_lower and 'ambiental' in collection:
                score += 1
            
            if score > 0:
                scored_chunks.append({
                    'chunk': chunk,
                    'score': score,
                    'citation': chunk.get('citation', 'Sin cita'),
                    'document': chunk.get('document_title', 'Sin título'),
                    'article': chunk.get('article', ''),
                    'text_preview': chunk_text[:200] + '...' if len(chunk_text) > 200 else chunk_text
                })
        
        # Ordenar por score y tomar top_k
        scored_chunks.sort(key=lambda x: x['score'], reverse=True)
        return scored_chunks[:top_k]
    
    def get_relevant_context(self, query: str, top_k: int = 5) -> str:
        """Obtener contexto relevante formateado para el prompt"""
        results = self.semantic_search(query, top_k)
        
        if not results:
            return "No se encontraron documentos normativos relevantes para la consulta."
        
        context_parts = []
        context_parts.append("📚 DOCUMENTOS NORMATIVOS RECUPERADOS:")
        
        for i, result in enumerate(results, 1):
            chunk = result['chunk']
            context_parts.append(f"\n{i}. {chunk.get('document_title', 'Sin título')}")
            context_parts.append(f"   📄 {chunk.get('citation', 'Sin cita')}")
            
            # Incluir estructura si existe
            if chunk.get('title'):
                context_parts.append(f"   📑 Título: {chunk['title']}")
            if chunk.get('article'):
                context_parts.append(f"   ⚖️ Artículo: {chunk['article']}")
            if chunk.get('article_heading'):
                context_parts.append(f"   📝 Encabezado: {chunk['article_heading']}")
            
            # Texto normativo (limitado)
            text = chunk.get('text', '')
            if len(text) > 500:
                text = text[:500] + "..."
            context_parts.append(f"   📋 Texto: {text}")
        
        context_parts.append("\n" + "="*80)
        context_parts.append("INSTRUCCIÓN: Usa SOLO la información de los documentos anteriores.")
        context_parts.append("Si la información no está en los documentos, indica: 'No se encontró fundamento en los documentos normativos disponibles.'")
        
        return "\n".join(context_parts)
    
    def extract_legal_ids(self, results: List[Dict]) -> List[str]:
        """Extraer IDs jurídicos de los chunks recuperados"""
        ids = []
        for result in results:
            chunk = result['chunk']
            # Buscar ID en metadatos
            for key in ['id_juridico', 'id', 'juridical_id']:
                if key in chunk and chunk[key]:
                    ids.append(chunk[key])
                    break
        return ids
    
    def get_documents_consulted(self, results: List[Dict]) -> List[str]:
        """Obtener lista de documentos consultados"""
        docs = set()
        for result in results:
            doc = result['chunk'].get('document_title', '')
            if doc:
                docs.add(doc)
        return list(docs)
    
    def get_articles_cited(self, results: List[Dict]) -> List[str]:
        """Obtener lista de artículos citados"""
        articles = []
        for result in results:
            chunk = result['chunk']
            doc = chunk.get('document_title', '')
            art = chunk.get('article', '')
            if doc and art:
                articles.append(f"{doc}, Art. {art}")
        return articles


# Instancia global para uso en la app
rag_engine = RAGEngine()

if __name__ == "__main__":
    # Test del motor RAG
    engine = RAGEngine()
    
    test_queries = [
        "Un restaurante tiene música muy fuerte hasta la madrugada",
        "Una obra sin permiso de construcción",
        "Comercio ambulante en vía pública"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: {query}")
        results = engine.semantic_search(query, top_k=3)
        print(f"📊 Resultados encontrados: {len(results)}")
        
        for i, result in enumerate(results, 1):
            print(f"  {i}. Score: {result['score']:.2f} - {result['citation']}")
            print(f"     Doc: {result['document']}")
            print(f"     Preview: {result['text_preview'][:100]}...")