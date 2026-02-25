# Invoice Extraction Bot

An AI-powered Streamlit application that automatically extracts key data fields from uploaded PDF invoices using Azure OpenAI — and exports the results as a downloadable CSV file.

---

## Overview

This tool allows users to upload one or multiple PDF invoices and automatically extracts structured data fields such as invoice number, description, quantity, date, unit price, amount, total, email, phone number, and address. The extracted data is displayed as a table and can be downloaded as a CSV file.

---

## Features

-  Upload single or multiple PDF invoices at once
-  AI-powered data extraction using Azure OpenAI
-  Extracted data displayed as a structured table
-  Download extracted data as a CSV file
-  Fast batch processing of multiple invoices

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| LLM | Azure OpenAI (Chat model) |
| PDF Parsing | PyPDF2 |
| Data Processing | Pandas |
| Prompt Orchestration | LangChain Core |

---

## Extracted Fields

| Field | Description |
|---|---|
| Invoice no. | Unique invoice identifier |
| Description | Item or service description |
| Quantity | Number of units |
| Date | Invoice date |
| Unit price | Price per unit |
| Amount | Line item total |
| Total | Overall invoice total |
| Email | Contact email address |
| Phone number | Contact phone number |
| Address | Billing or shipping address |

---

## Project Structure
```
├── app.py              # Main Streamlit UI and app entry point
├── utils.py            # PDF parsing, LLM extraction, and DataFrame logic
├── test.py             # Test file
├── requirements.txt    # Python dependencies
└── README.md
```

---

## Prerequisites

- Python 3.9+
- An [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service) account with a chat model deployment (e.g., `gpt-4o` or `gpt-35-turbo`)

---

## Installation

**1. Clone the repository**
```bash
git clone <your-repo-url>
cd <repo-folder>
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure secrets**

Create a `.streamlit/secrets.toml` file in the project root:
```toml
AZURE_OPENAI_ENDPOINT   = "https://your-resource.openai.azure.com/"
AZURE_OPENAI_API_KEY    = "your-azure-openai-api-key"
AZURE_OPENAI_DEPLOYMENT = "your-chat-deployment-name"
```

---

## Usage

**1. Run the app**
```bash
streamlit run app.py
```

**2. In the browser UI:**
- Upload one or more **PDF invoice files**
- Click **"Extract Data"**
- View the extracted data in a **table preview**
- Click **"Download data as CSV"** to save the results

---

## How It Works
```
PDF Invoices (uploaded)
      ↓
PyPDF2 → Raw Text Extraction
      ↓
Azure OpenAI → Structured Data Extraction via Prompt
      ↓
Regex + ast.literal_eval → Parse LLM Response into Dict
      ↓
Pandas DataFrame → Aggregated Results Table
      ↓
Streamlit UI → Preview + CSV Download
```

1. Each uploaded PDF is read using `PyPDF2` to extract raw text.
2. The raw text is passed to Azure OpenAI with a structured extraction prompt.
3. The LLM returns a dictionary-like string with the extracted fields.
4. A regex pattern and `ast.literal_eval` parse the response into a Python dictionary.
5. All extracted records are compiled into a Pandas DataFrame.
6. The DataFrame is displayed in the UI and made available for CSV download.

---

## Notes

> - Only **PDF files** are accepted for upload.
> - If the LLM response cannot be parsed, that invoice is skipped and an empty row is added.
> - `temperature` is set to `0.9` — lower it in `utils.py` for more deterministic extraction results.
> - The downloaded CSV is named `benchmark-tools.csv` by default — update this in `app.py` as needed.

---
End of Documentation
---
