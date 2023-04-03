import openai
import llama_index
from llama_index import LLMPredictor, GPTSimpleVectorIndex, PromptHelper
import openai
import streamlit as st
import os
from pathlib import Path
from gpt_index import download_loader

BASE_PROMPT = [{"role": "system", "content": "You are a helpful assistant."}]

if "messages" not in st.session_state:
    st.session_state["messages"] = BASE_PROMPT
    
def show_messages(text):
    messages_str = [
        f"{_['role']}: {_['content']}" for _ in st.session_state["messages"][1:]
    ]
    text.text_area("Messages", value=str("\n".join(messages_str)), height=250)

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

# define LLM
#llm_predictor = LLMPredictor(llm=openai(temperature=0.1, model_name="text-davinci-002"))
# define prompt helper
# set maximum input size
#max_input_size = 4096
# set number of output tokens
#num_output = 256
# set maximum chunk overlap
#max_chunk_overlap = 20
#prompt_helper = PromptHelper(max_input_size, num_output, max_chunk_overlap)
#custom_LLM_index = GPTSimpleVectorIndex(
#    documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper
#)


#from llama_index import SimpleDirectoryReader
#from llama_index import download_loader
#WikipediaReader = download_loader("WikipediaReader")
#loader = WikipediaReader()
#wikidocs = loader.load_data(pages=['Simon Wardley'])
#wiki_index = GPTSimpleVectorIndex.from_documents(wikidocs)
#response = wiki_index.query("Who is Simon Wardley?")
#print(response)

#YoutubeTranscriptReader = download_loader("YoutubeTranscriptReader")
#loader = YoutubeTranscriptReader()
#documents = loader.load_data(ytlinks=['https://www.youtube.com/watch?v=7GDeG3Yf9r4'])
#index = GPTSimpleVectorIndex.from_documents(documents)
#response = index.query("What is wardley mapping")
#print(response)

st.video('https://youtu.be/L3wgzl2iUR4') 

text = st.empty()
show_messages(text)

prompt = st.text_input("Prompt", value="What is this video about?")

if st.button("Send"):
    with st.spinner("Generating response..."):
        
        #st.session_state["messages"] += [{"role": "user", "content": prompt}]
        #response = openai.ChatCompletion.create(
        #    model="gpt-3.5-turbo", messages=st.session_state["messages"]
        #)
        
        response = index.query(prompt)
        #response = index.query(messages=st.session_state["messages"])
        #st.write (response)
        
        message_response = response["choices"][0]["message"]["content"]
        st.session_state["messages"] += [
            {"role": "system", "content": message_response}
        ]
        show_messages(text)
        text.text_area("Messages", response, height=250)

if st.button("Clear"):
    st.session_state["messages"] = BASE_PROMPT
    show_messages(text)
