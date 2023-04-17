import openai
import llama_index
from llama_index import LLMPredictor, GPTSimpleVectorIndex, PromptHelper
import openai
import streamlit as st
import os
from pathlib import Path
from gpt_index import download_loader

BASE_PROMPT = [{"role": "system", "content": "You are a helpful assistant."}]

openai.api_key = st.secrets["OPENAI_API_KEY"]

YoutubeTranscriptReader = download_loader("YoutubeTranscriptReader")
loader = YoutubeTranscriptReader()
documents = loader.load_data(ytlinks=['https://www.youtube.com/watch?v=L3wgzl2iUR4'])

index = GPTSimpleVectorIndex.from_documents(documents)

st.set_page_config(page_title="Intro To Wardley Mapping with AI")
st.title("Intro To Wardley Mapping with AI")
st.sidebar.markdown("# Query this video using AI")

st.sidebar.markdown("Developed by Mark Craddock](https://twitter.com/mcraddock)", unsafe_allow_html=True)
st.sidebar.markdown("Current Version: 0.0.2")

st.video('https://youtu.be/L3wgzl2iUR4') 

text = st.empty()

prompt = st.text_input("Prompt", value="What is this video about?")

if st.button("Send"):
    with st.spinner("Generating response..."):
        
        response = index.query(prompt)
        text.text_area("Messages", response, height=250)

if st.button("Clear"):
    st.session_state["messages"] = BASE_PROMPT
    show_messages(text)
