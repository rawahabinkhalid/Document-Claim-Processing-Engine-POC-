from langchain.tools import tool
from crewai_tools import PDFSearchTool
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
import os
import httpx


class RAGTools():

    @tool("PDF RAG Tool")
    def search_pdf(pdf_path: str, query: str):
        """Useful to perform RAG operations on PDF documents based on query
        """
        try:
            return PDFSearchTool(pdf=pdf_path,
                                 config=dict(
                                     llm=dict(
                                         provider="azure_openai",  # or google, openai, anthropic, llama2, ...
                                         config=dict(
                                             model=os.environ.get("AZURE_MODEL_NAME"),
                                             deployment_name=os.environ.get("AZURE_MODEL_DEPLOYMENT"),
                                             api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
                                         ),
                                     ),
                                     embedder=dict(
                                         provider="azure_openai",  # or openai, ollama, ...
                                         config=dict(
                                             model=os.environ.get("AZURE_TEXT_MODEL_NAME"),
                                             deployment_name=os.environ.get("AZURE_TEXT_MODEL_DEPLOYMENT"),
                                             api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
                                         ),
                                     ),
                                 )
                                 ).run(query)
        except FileNotFoundError:
            return "Error: PDF file no found!"
        except Exception as e:
            return f"{e}"
