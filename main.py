from crewai import Crew, Process
from tempfile import NamedTemporaryFile
from textwrap import dedent
from claim_agents import ClaimAgents
from claim_tasks import ClaimTasks
import streamlit as st
from dotenv import load_dotenv
import os
st.set_page_config(layout="wide")
load_dotenv()


class ClaimCrew:

    def __init__(self, receipt_path, health_policy_path):
        self.receipt_path = receipt_path
        self.health_policy_pdf_path = health_policy_path

    def run(self):
        agents = ClaimAgents()
        tasks = ClaimTasks()

        receipt_analyst = agents.receipt_analysis_agent()
        internet_research_agent = agents.research_expert()
        claim_officer = agents.claim_expert()

        receipt_identification_task = tasks.identify_receipt_task(
            receipt_analyst,
            self.receipt_path)

        internet_research_task = tasks.research_task(internet_research_agent)
        claim_task = tasks.claim_report_task(
            claim_officer,
            self.health_policy_pdf_path
        )

        crew = Crew(
            agents=[
                receipt_analyst,
                internet_research_agent,
                claim_officer
            ],
            tasks=[receipt_identification_task,
                   internet_research_task,
                   claim_task
                   ],
            output_log_file="./crew_logs.txt",
            process=Process.sequential,
            memory=True,
            embedder=dict(
                provider="azure_openai",  # or openai, ollama, ...
                config=dict(
                    model=os.environ.get("AZURE_TEXT_MODEL_NAME"),
                    deployment_name=os.environ.get("AZURE_TEXT_MODEL_DEPLOYMENT"),
                    api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
                ),
            ),
            verbose=True
        )

        result = crew.kickoff()
        return result


if __name__ == "__main__":
    st.title("Welcome to Claim Analysis Portal")
    uploaded_file = st.file_uploader("Upload consultancy/lab tests/medicines slips only in .png or .jpg",
                                     type=['png', 'jpg'], key="upload_id", help="Upload file!")
    pdf_path = "Documents/HealthCare_Policy.pdf"
    if uploaded_file is not None:
        st.subheader("File: ")
        if '.pdf' in uploaded_file.name:
            pass
        else:
            st.image(uploaded_file)
            try:
                with NamedTemporaryFile(dir='.', delete=False) as f:
                    f.write(uploaded_file.getbuffer())
                    image_path = f.name
                    trip_crew = ClaimCrew(image_path, pdf_path)
                    result = trip_crew.run()
                    st.write("Claim Analysis:", result)
            except Exception as e:
                st.write(e)
