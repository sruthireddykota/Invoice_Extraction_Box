from langchain_openai import AzureChatOpenAI
import streamlit as st
from PyPDF2 import PdfReader
import pandas as pd
import re
import ast
from langchain_core.prompts import ChatPromptTemplate

def get_pdf_text(pdf_doc):
    text = ""
    pdf_reader = PdfReader(pdf_doc)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extracted_data(pages_data):
    template = """Please Extract all the following values : invoice no., Description, Quantity, date, 
        Unit price , Amount, Total, email, phone number and address from this data: {pages}

        Expected output: remove any dollar symbols {{'Invoice no.': '1001329','Description': 'Office Chair','Quantity': '2','Date': '5/4/2023','Unit price': '1100.00','Amount': '2200.00','Total': '2200.00','Email': 'Santoshvarma0988@gmail.com','Phone number': '9999999999','Address': 'Mumbai, India'}}
        """
    prompt_template = ChatPromptTemplate.from_template(template)

    llm = AzureChatOpenAI(
        azure_endpoint=st.secrets["AZURE_OPENAI_ENDPOINT"],       
        openai_api_key=st.secrets["AZURE_OPENAI_API_KEY"],
        openai_api_version="2024-06-01",
        model_name=st.secrets["AZURE_OPENAI_DEPLOYMENT"], 
        temperature=0.9
    )
    full_prompt = prompt_template.format_messages(pages=pages_data)

    response = llm.invoke(full_prompt)
    
    return response.content 

def create_docs(user_pdf_list):
    df = pd.DataFrame({
        'Invoice no.': pd.Series(dtype='str'),
        'Description': pd.Series(dtype='str'),
        'Quantity': pd.Series(dtype='str'),
        'Date': pd.Series(dtype='str'),
        'Unit price': pd.Series(dtype='str'),
        'Amount': pd.Series(dtype='str'), 
        'Total': pd.Series(dtype='str'),
        'Email': pd.Series(dtype='str'),
        'Phone number': pd.Series(dtype='str'),
        'Address': pd.Series(dtype='str')
    })
    
    for filename in user_pdf_list:
        print(filename)
        raw_data = get_pdf_text(filename)
        print("extracted raw data")

        llm_extracted_data = extracted_data(raw_data)

        pattern = r'\{(.+)\}'
        match = re.search(pattern, llm_extracted_data, re.DOTALL)
        if match:
            extracted_text = match.group(1)
            try:
                data_dict = ast.literal_eval('{' + extracted_text + '}')
                print(data_dict)
            except:
                print("Could not parse extracted data")
                data_dict = {}
        else:
            print("No match found.")
            data_dict = {}
        df = pd.concat([df, pd.DataFrame([data_dict])], ignore_index=True)
        print("********************DONE***************")
    
    return df