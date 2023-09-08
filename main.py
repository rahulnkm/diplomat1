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

# SETUP API KEYS
with st.expander("1: API Keys & Personal statement"):
    openai_api_key = st.text_input("OpenAI API key", placeholder="sk-abc123...")
    openai.api_key = openai_api_key

    # PERSONAL STATEMENT
    personal_statement = st.text_area("Personal statement",
                                      placeholder="I'm a 22 yr old software engineer at a blockchain startup. I studied computer science and anthropology at DeVry University. My hobbies include playing with my cat, rock climbing, and working on model planes. I live in San Francisco. I also buy NFTs, participate in DAOs, and listen to podcasts.")
    
    # TOGGLE MODEL
    toggle_model = st.radio(
        "Select LLM model",
        ["gpt-4-32k", "gpt-3.5-turbo-16k"],
        captions = ["Better but slower", "Faster but worse"])

    # TOGGLE PERSONALITY - BENNY GIANG / GET VARIANT FUND RECOMMENDATION
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
        You are a cute cat. Start and end sentences with meow, miaou, miaw, and nyan. Show an appreciation for things cats like (yarn, milk, naps).
        Speak super adorably and cutely. 
        """
    elif toggle_voice == "Bored Ape Yacht Club":
        voice_statement = """
        You are a bored ape that lives on a yacht. You are so rich you don't care about money.
        You're also a little immature and a self-proclaimed "degenerate."
        Make jokes with potty humor. Or be a little crass.
        """
    elif toggle_voice == "Azuki":
        voice_statement = """
        You're a cool, stoic ninja. Act like an action hero and make quips.

        """
    elif toggle_voice == "Milady Maker":
        voice_statement = """
        You're an insane psychopath that speaks in tongues.
        You are only barely able to be understood by the listener.

        """

    # DAO CONSTITUTION
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

with st.expander("2: Connect your accounts"):
    eth_address = st.text_input("ETH address")
    farcaster = st.text_input("Farcaster username")

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
            return st.write(vector)
        
def get_farcaster_report(farcaster_embeddings):
    return report


# ---------- GENERATE REPORT ---------------------------------
system_prompt = f"""There is a person. This is their description: {personal_statement}.
    
    You are their personal representative. You are tasked with passing proposals that are aligned with their interests.
    
    Respond True if you would pass the law, False if you would reject the law and Not enough info if there is not enough info.
    
    Include your reasoning. Ask questions if there is not enough info to clarify a Yes/No answer.
    
    They belong to a DAO, or organization. Make sure you keep their interests in mind as well. Their stipulations and description are: {dao_statement}.
    
    You also should speak with the following personality: {voice_statement}.
    
    There is a proposal. Its description is: {manual_proposal}."""

if st.checkbox("View full prompt"):
    st.caption(system_prompt)

def GenerateReport(proposal):
    result = openai.ChatCompletion.create(
        model=toggle_model,
        messages=[
            {"role": "user", "content": system_prompt}
            ]
        )
    report = result['choices'][0]['message']['content']
    return report

if st.button("Generate report"):
    # st.write(GenerateTone(manual_proposal))
    st.markdown(GenerateReport(system_prompt))
    searchcaster_embeddings("gigarahul")

# STORE IN DATABASE


# def create_proposal