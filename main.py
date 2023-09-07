import streamlit as st
import openai
import json
import supabase
import requests
import re

# OPEN SOURCE: 

with st.expander("Add personal info here"):
    eth_address = st.text_input("ETH address")
    openai_api_key = st.text_input("OpenAI API key")
    personal_statement = st.text_area("Personal statement")
    # conditional_statements = st.text_area("")

# STORE IN DATABASE


# def create_proposal


def PersonalAgent():
        system_prompt = f"""
        You are a professional profiler who wants to describe a person for a lawyer.
        Describe the kind of values and interests this person might have.
        You have to describe this person for a jury. The jury will make a decision for the person.
        """
        result = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt}, # Bot is representative
                {"role": "user", "content": person}
                ]
            )
        return result['choices'][0]['message']['content']