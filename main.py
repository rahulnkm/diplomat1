import streamlit as st
import streamlit_authenticator as stauth
import openai
import json
import supabase
import requests
import re

# Generate a personalized suggestion for voting on DAO proposals
# 1. Webhook
# 2. Email
# 3. User data

# DO: webhook

st.header("Diplomat Settings")
st.markdown("A fast and informed personalized voting suggestion for every DAO proposal, powered by LLMs.")

with st.expander("1: API Keys & Personal statement"):
    openai_api_key = st.text_input("OpenAI API key", placeholder="sk-abc123...")
    openai.api_key = openai_api_key
    personal_statement = st.text_area("Personal statement",
                                      placeholder="I'm a software engineer who likes AI, crypto, communities, and cats.")
    toggle_model = st.radio(
    "Select LLM model",
    ["gpt-4-32k", "gpt-3.5-turbo-16k"],
    captions = ["Better but slower", "Faster but worse"])

    # BENNY GIANG - VARIANT FUND RECOMMENDATION

    toggle_voice = st.radio(
    "Select voice",
    ["None", "CryptoKitties", "Bored Ape Yacht Club", "Azuki", "Milady Maker"],
    captions = ["Your standard AI helper", "Meow meow miaou", "Dude, wen lambo?", "The coolest around", "m̴̛̜͔̻͓̮̦͓̮̗̲͗̃̏̒̈́̿͝ḭ̸̧̠̘̠̹͚͇̮̈́̽́̈́̋̆͝l̷͕̜͔͙̪͎̲̩͚̺̰̀͊̃̎̎̒̾̌͑̓̿̐͝ä̸̢͖͍̻̦́͂̅̋͑͗̈́͊͝ḋ̶̬̯̱͉̰̠̠̖̖͙̳̄y̴̨̧̹͚͇͓̦̳̎̌̍̐̊͆͂̚̕͠ͅ ̵̨̭͖̳̐͛̇̿̊͊̄̉̏͛̚̚m̶̢̝̻̙̦̣̍a̵̘͔̖͔̦͖̗̪͍͚̦̲͐͆̒͘͜ͅķ̴̼͎̯̝̈́͒̀̉͊͑́̑̕͜e̶̺͙͔̗̠͎̎̐̀̓̽͂̽ŗ̶̦̘̣͐͘"])
    voice_statement = ""
    if toggle_voice == "None":
        voice_statement = """
        Make no adjustments to the voice of the report.
        """
    elif toggle_voice == "CryptoKitties":
        voice_statement = """
        You are a cat. Say meow and other original meow variants (miaou, miaw, nyan) when appropriate. Show an appreciation for things cats like.
        """
    elif toggle_voice == "Bored Ape Yacht Club":
        voice_statement = """
        You are an ape that is so rich you don't care about money. You're also a little immature and a self-proclaimed "degenerate." 
        """
    elif toggle_voice == "Azuki":
        voice_statement = """
        You're a cool, stoic ninja. 
        """
    elif toggle_voice == "Milady Maker":
        voice_statement = """
        You're an insane psychopath that speaks in tongues. You are only barely able to be understood by the listener.
        """

    toggle_dao = st.radio(
    "Select DAO",
    ["Aave", "Nouns DAO", "Purple DAO"],
    captions = ["Lending and borrowing", "Spread the meme!", "Farcaster 4eva"])
    dao_statement = ""
    if toggle_dao == "None":
        dao_statement = "There is no DAO."
    elif toggle_dao == "Aave":
        dao_statement = """
        Aave is a crypto protocol that focuses on lending and borrowing.
        The purpose of the DAO is to decentralize the power and enable users to contribute towards the development of the protocol by voting.
        We must prioritize our long term stability and safety to our protocols.
        """
    elif toggle_dao == "Nouns DAO":
        dao_statement = """
        The purpose of the DAO is to spread the meme so that more people will bid on the new Nouns every day.
        """
    elif toggle_dao == "Purple DAO":
        dao_statement = """
        The purpose of the DAO is to fund projects that improve and promote the Farcaster protocol.
        """


def get_eth_details():
    return eth_details

with st.expander("2: Add optional data here"):
    eth_address = st.text_input("ETH address")
    farcaster = st.text_input("Farcaster username")
    # conditional_statements = st.text_area("")
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
        
def get_farcaster_report(farcaster_embeddings):
    return report


# ---------- GENERATE REPORT ---------------------------------

def GenerateReport(proposal):
    system_prompt = f"""There is a person. This is their description: {personal_statement}
    You are their personal representative. You are tasked with passing laws that are aligned with their interests.
    Respond True if you would pass the law, False if you would reject the law and Not enough info if there is not enough info.
    Include your reasoning. Ask questions if there is not enough info to clarify a Yes/No answer.
    They belong to a DAO. Their stipulations and description is: {dao_statement}
    You have to respond in a voice. The details are as such: {voice_statement} 
    There is a proposal. Its description is: {proposal}"""
    result = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": system_prompt}
            ]
        )
    report = result['choices'][0]['message']['content']
    return report

if st.button("Generate report"):
    st.markdown(GenerateReport(manual_proposal))

# STORE IN DATABASE


# def create_proposal