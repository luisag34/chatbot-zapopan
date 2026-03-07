from setuptools import setup, find_packages

setup(
    name="chatbot-zapopan",
    version="1.0.0",
    description="Sistema de Consulta Normativa para el Ayuntamiento de Zapopan",
    author="Luis Alberto Aguirre Gómez",
    author_email="luis.aguirre34@gmail.com",
    packages=find_packages(),
    install_requires=[
        "streamlit==1.55.0",
        "pandas==2.3.3",
        "numpy==2.4.2",
        "google-genai==0.8.6",
        "requests==2.32.5",
    ],
    python_requires=">=3.9",
)