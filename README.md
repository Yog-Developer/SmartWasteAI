
# SmartWaste AI

A Generative AI-powered cloud-based food waste reduction assistant for restaurants.

## Overview

SmartWaste AI helps restaurants manage ingredient inventory, identify items approaching expiry, and generate practical recommendations to reduce avoidable food waste.

This project was developed as part of Problem-cum-Project Based Learning (PPBL-1) for the course Introduction to Cloud Computing for Managers at UPES.

## Features

- Ingredient inventory management
- Automatic expiry status calculation
- Colour-coded inventory dashboard
- AI-powered recipe generation
- Food waste reduction suggestions
- Daily inventory reports
- CSV dataset export
- AI performance monitoring

## Technology Stack

- Frontend: Streamlit
- Backend: Python
- Data processing: Pandas
- Generative AI: GPT-5 mini
- AI platform: Microsoft Foundry / Azure OpenAI
- Hosting: Azure App Service (Linux, Basic B1)
- Cloud region: UAE North
- Service model: PaaS
- Deployment model: Public Cloud
- Version control: Git and GitHub

## Local Setup

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install the dependencies:

   pip install -r requirements.txt

4. Copy .env.example to .env and configure your Azure credentials.
5. Test the Azure connection:

   python check_azure.py

6. Run the application:

   python -m streamlit run app.py

## Initial Cloud Testing Results

| Metric | Result |
|---|---|
| AI requests tested | 3 |
| Successful requests | 3 |
| AI request success rate | 100% |
| Average response time | 16.18 seconds |
| Recipe generation | 19.50 seconds |
| Waste reduction | 13.07 seconds |
| Daily report | 15.96 seconds |

These results represent a limited prototype test and do not establish production reliability or AI accuracy.

## Estimated Cloud Cost

- Azure App Service: $16.06/month
- Azure OpenAI: $2.25/month
- Total estimated cost: $18.31/month

The estimate assumes 730 hosting hours and one million input and output tokens each per month. AI pricing uses East US reference rates. Actual billing may vary.

## Limitations

- Uses fictional restaurant inventory data.
- Inventory is stored temporarily within the session.
- No persistent database or user authentication.
- AI recommendations may contain inaccuracies.
- Actual food waste reduction and financial savings have not been measured.
- Not a food-safety verification system.

## Team Members

- Yog Pandey - Project Coordinator
- Priyanshu Kaushik - Research Lead
- Lakshya Dhyani - Business and Stakeholder Lead
- Chaitanya Dev Sharma - Technical Lead

## Academic Disclosure

Generative AI tools were used to assist with development, debugging, documentation and Azure deployment guidance.
