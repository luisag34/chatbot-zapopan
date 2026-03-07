from setuptools import setup, find_packages

setup(
    name="chatbot-zapopan",
    version="1.0.0",
    description="Sistema de Consulta Normativa para el Ayuntamiento de Zapopan",
    author="Luis Alberto Aguirre Gómez",
    author_email="luis.aguirre34@gmail.com",
    packages=find_packages(),
    install_requires=[
        "streamlit==1.28.1",
        "pandas==2.1.4",
        "numpy==1.24.4",
        "google-generativeai==0.3.2",
        "plotly==5.18.0",
        "python-dotenv==1.0.0",
        "requests==2.31.0",
    ],
    python_requires=">=3.9",
)