# Document Claim Processing Engine (POC)

## Overview

The **Document Claim Processing Engine (POC)** is an application designed to analyze medical receipts (consultation fees, medicines bills, lab tests) and determine their eligibility for claim approval based on a predefined healthcare policy. The application uses various AI agents to perform tasks like receipt analysis, internet research, and claim evaluation.

## Features

- **Receipt Analysis**: Identifies the type of receipt (consultation fee, medicines bill, or lab tests) from an uploaded image.
- **Internet Research**: Gathers detailed information about the items listed in the receipt.
- **Claim Evaluation**: Calculates and determines the eligibility of the claim based on the company’s healthcare policy.

## Requirements

- **Python 3.8+**
- **Streamlit**: For the web interface.
- **Crew AI**: For orchestrating tasks between different AI agents.
- **Azure OpenAI**: For utilizing Azure's language models.
- **httpx**: For HTTP client interactions.
- **dotenv**: For managing environment variables.

## Setup

### Environment Variables

Create a `.env` file in the root directory and add your Azure OpenAI credentials:

```
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_MODEL_DEPLOYMENT=your_azure_model_deployment_name
AZURE_OPENAI_API_VERSION=your_azure_openai_api_version
AZURE_TEXT_MODEL_NAME=your_azure_text_model_name
AZURE_TEXT_MODEL_DEPLOYMENT=your_azure_text_model_deployment
```

### Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### Running the Application

To start the application, run:

```bash
streamlit run app.py
```

## Usage

1. **Upload Receipt**: On the homepage, upload a receipt image file (PNG or JPG format) that you wish to analyze.
2. **View Analysis**: Once the file is uploaded, the application will process it and display the analysis results, including the type of receipt, item details, and claim approval status.

## Project Structure

- **app.py**: The main Streamlit application script.
- **crewai.py**: Contains the definition of the AI agents and tasks used in the claim analysis process.
- **Documents/HealthCare_Policy.pdf**: The healthcare policy document used for evaluating claims.
- **crew_logs.txt**: Log file generated during the claim processing.

## AI Agents

### Receipt Analysis Expert

- **Goal**: Analyze and identify the type of receipt.
- **Tools**: VisionTools for image analysis.

### Internet Research Expert

- **Goal**: Gather accurate information about the products and their uses listed in the receipt.
- **Tools**: SearchTools for internet research.

### Expert Claim Officer

- **Goal**: Evaluate and approve or deny the claim based on the healthcare policy.
- **Tools**: RAGTools for PDF searching, CalculatorTools for calculations.

## Logs

The processing of claims is logged in `crew_logs.txt` for debugging and auditing purposes.

## Tips

- Ensure that the healthcare policy PDF is correctly formatted and accessible at the specified path.
- Uploaded images should be clear and well-lit for accurate analysis.

## Troubleshooting

- **Errors in Image Upload**: Ensure the image is in PNG or JPG format.
- **Azure API Errors**: Verify your API credentials and check the `.env` file.

## License

This project is licensed under the MIT License - see the LICENSE file for details.