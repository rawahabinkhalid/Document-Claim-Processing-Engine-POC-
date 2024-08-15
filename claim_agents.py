from crewai import Agent
from crewai_tools import PDFSearchTool
from langchain_openai import AzureChatOpenAI
from tools.browser_tools import BrowserTools
from tools.calculator_tools import CalculatorTools
from tools.search_tools import SearchTools
from tools.vision_tool import VisionTools
from tools.rag_tools import RAGTools
import os
import httpx

os.environ["OTEL_SDK_DISABLED"] = "true"


class ClaimAgents():
    def __init__(self):
        self.azure_llm = AzureChatOpenAI(
            azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
            api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
            azure_deployment=os.environ.get("AZURE_MODEL_DEPLOYMENT"),
            api_version=os.environ.get("AZURE_OPENAI_API_VERSION"),
            http_client=httpx.Client(verify=False),
            max_tokens=1000,
            max_retries=10)

    def receipt_analysis_agent(self):
        return Agent(
            role='Receipt Analysis Expert',
            goal='Analyze consultation fee, medicines and lab tests receipt',
            backstory=
            'An expert in analyzing claim receipt data',
            tools=[
                VisionTools.analyze_image,
            ],
            llm=self.azure_llm,
            allow_delegation=False,
            verbose=True)

    def research_expert(self):
        return Agent(
            role='Internet Research Expert',
            goal='Research and provide accurate information about the products and their uses',
            backstory="""A professional internet explorer with attention to details""",
            tools=[
                SearchTools.search_internet,
#                BrowserTools.scrape_and_summarize_website,
            ],
            llm=self.azure_llm,
            allow_delegation=False,
            verbose=True)

    #
    def claim_expert(self):
        return Agent(
            role='Expert Claim Officer',
            goal="""Calculate and approve medical claims according to company's health policy""",
            backstory="""Specialist in evaluating medical claims""",
            tools=[
                RAGTools.search_pdf,
                CalculatorTools.calculate
            ],
            llm=self.azure_llm,
            allow_delegation=False,
            verbose=True)
