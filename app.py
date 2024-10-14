from dotenv import load_dotenv
load_dotenv() # Load all environment variables from .env

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# FUnction to load Gemini Pro Vision
model=genai.GenerativeModel('gemini-1.5-flash')

def get_gemini_response(input,image,prompt):
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        # Read file into bytes
        bytes_data=uploaded_file.getvalue()
        
        image_parts=[
            {
                "mime_type":uploaded_file.type,
                "data":bytes_data
            }
        ]
        return image_parts

# Initiate streamlit application
st.set_page_config(page_title="Invoice Extractor")

st.header("Gemini APplication")
input=st.text_input("Input Prompt:",key="input")
uploaded_file=st.file_uploader("Choose an image of the invoice...",type=["jpg","jpeg","png"])
image=""
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image",use_column_width=True)

submit=st.button("Tell me about the invoice")

input_prompt="""
You are an expert in understanding invoices. We will upload image as invoice and you will have to answer any questions based on 
the uploaded invoice image
"""

# If submit button is clicked
if submit:
    image_date=input_image_details(uploaded_file)
    response=get_gemini_response(input_prompt,image_date,input)
    st.subheader("The response is")
    st.write(response)