import streamlit as st
import openai
import json
import supabase
import requests
import re

# OPEN SOURCE: 

with st.expander("1: API Keys & Personal statement"):
    openai_api_key = st.text_input("OpenAI API key")
    openai.api_key = openai_api_key
    personal_statement = st.text_area("Personal statement", placeholder="I'm a 22 year old guy who likes AI, crypto, communities, and cats.")
    # conditional_statements = st.text_area("")

with st.expander("2: Add optional data here"):
    eth_address = st.text_input("ETH address")

manual_proposal = st.text_area("go")

def GenerateReport(proposal):
    system_prompt = f"""There is a person. This is their description: {personal_statement}
    You are their personal representative. You are tasked with passing laws that are aligned with their interests. Respond True if you would pass the law, False if you would reject the law and Not enough info if there is not enough info. Include your reasoning. Ask questions if there is not enough info to clarify a Yes/No answer.
    There is a proposal. Its description is: {proposal}"""
    result = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt}, # Bot is representative
            {"role": "user", "content": personal_statement}
            ]
        )
    report = result['choices'][0]['message']['content']
    return report

if st.button("Generate report"):
    st.markdown(GenerateReport(manual_proposal))

# STORE IN DATABASE


# def create_proposal