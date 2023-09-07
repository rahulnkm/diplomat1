import streamlit as st
import openai
import json
import supabase
import requests
import re

# Generate a personalized suggestion for voting on DAO proposals
# 1. Webhook
# 2. Email
# 3. User data 

with st.expander("1: API Keys & Personal statement"):
    openai_api_key = st.text_input("OpenAI API key")
    openai.api_key = openai_api_key
    personal_statement = st.text_area("Personal statement",
                                      placeholder="I'm a software engineer who likes AI, crypto, communities, and cats.")
    toggle_model = st.radio(
    "Select LLM model",
    ["GPT 4", "GPT 3"],
    captions = ["Better but slower", "Faster but worse"])

def get_eth_details():
    return eth_details

with st.expander("2: Add optional data here"):
    eth_address = st.text_input("ETH address")
    farcaster = st.text_input("Farcaster username")
    if eth_address:
        st.caption()

manual_proposal = st.text_area("Enter proposal text")

def searchcaster_embeddings(username):
        user = username
        if user == "" | user == None :
            return st.error('invalid username')
        
        NUMBER_OF_POSTS = 200  # max 200
        SEARCHCASTER_URL = "https://searchcaster.xyz/api/search"
        base_url = SEARCHCASTER_URL
        params = {"username": username}
        response = requests.get(base_url, params=params)
        if response.status_code != 200:
            return (f"Error: {response.status_code} - {response.text}")
        else:
            data = response.json()
            posts = data['casts']
            final = ""
            for i, post in enumerate(posts, 1):
                text = post['body']['data']['text']
                final = final + f"{text} \n"
            embedding = openai.Embedding.create(
                model="text-embedding-ada-002",
                input=final
                )
            vector = embedding['data'][0]['embedding']
            return vector

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