from crewai import Task
from textwrap import dedent
from tools.vision_tool import VisionTools
from datetime import date


class ClaimTasks():
    def identify_receipt_task(self, agent, receipt_path):
        return Task(description=dedent(f"""
                    Analyze and identify whether it is a consultation fee,
                    medicines bill or lab tests receipt. Otherwise, it a unknown type.
                    {self.__tip_section()}
            
                    image_path: {receipt_path}
                    """),
                    expected_output="Return Receipt type with explanation",
                    agent=agent)

    def research_task(self, agent):
        return Task(description=dedent(f"""
                    As a internet research expert gather accurate information about the 
                    medicines, lab tests and their uses listed in the receipt information
                    provided by Receipt Analysis Expert. 
            
                    Do not proceed in the case of unknown receipt type.
                    {self.__tip_section()}
                    """),
                    expected_output="""The final answer must be a comprehensive report 
                                        about the receipt type, items, categories, uses and purchase price per item mentioned 
                                        in the receipt.""",
                    agent=agent)

    def claim_report_task(self, agent, healthcare_policy_pdf_path):
        return Task(description=dedent(f"""
                As a Medical Claim Officer gather item's uses, purchase price information and 
                receipt type details provided by Internet Research Expert. Do not proceed if receipt type is unknown. 
                If the receipt type is consultation fee, simply approve.
                
                Use medicines or lab tests primary usage and category information (for example: pain killers, antibiotics e.t.c.) 
                and check whether it is covered under company's healthcare policy. Do not use item names.
                
                Only approve such claim items that are not excluded according to healthcare policy, otherwise do not approve.
                 
                Make accurate calculations on the approved items only and include in the final report, composed of 
                item names, claim amounts, approval status and reason why it is approved or not approved. Do not assume prices on your own.
                Use PKR as base currency while making calculations, prices are always in PKR so do not convert in dollars(USD).
                
                Construct final report in table format.
                
                {self.__tip_section()}
                
                healthcare_policy_pdf_path: {healthcare_policy_pdf_path}
                """),
                expected_output="""Your Final Answer must be a Final Report on Medical Claims Evaluation
                                including item names, claim amounts, approval status, reason why it is approved or not approved, 
                                totals, discounts and approved amount""",
                agent=agent)

    def __tip_section(self):
        return "If you do your BEST WORK, I'll tip you with a dinner party!"
