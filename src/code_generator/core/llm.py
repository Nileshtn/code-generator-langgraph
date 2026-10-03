from langchain_ollama import ChatOllama
from code_generator.config import model_config

core_llm = ChatOllama(model=model_config['model'], temperature=model_config['temp'])