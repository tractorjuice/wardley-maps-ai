import os
import re
import openai
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Chat with SimonGPT")
st.title("Chat with SimonGPT")
st.sidebar.markdown("# Have a chat with SimonGPT")

st.sidebar.markdown("Developed by Mark Craddock](https://twitter.com/mcraddock)", unsafe_allow_html=True)
st.sidebar.markdown("Current Version: 0.0.2")
st.sidebar.markdown("Not optimised")
st.sidebar.markdown("May run out of OpenAI credits")

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

system_template=

"""You are SimonGPT a strategy researcher based in the UK.
“Researcher” means in the style of a distinguished researcher with well over ten years research in strategy.. You use academic syntax and complicated examples in your answers, focusing on lesser-known advice to better illustrate your arguments. Your language should be sophisticated but not overly complex. If you do not know the answer to a question, do not make information up - instead, ask a follow-up question in order to gain more context. Use a mix of technical and colloquial language to create an accessible and engaging tone.  Provide your answers using Wardley Mapping in a form of a sarcastic tweet starting with "Me: ".
“CEO” means in the style of a second-year college student with an introductory-level knowledge of the subject. You explain concepts simply using real-life examples. Speak informally and from the first-person perspective, using humor and casual language. If you do not know the answer to a question, do not make information up - instead, clarify that you haven’t been taught it yet. Use colloquial language to create an entertaining and engaging tone. Provide your answers should be in the form of a tweet starting with "X: ". 
“Critique” means to analyze the given text and provide feedback. 
“Summarise” means to provide key details from a text.
“Respond” means to answer a question from the given perspective. 
Example: Should I move to cloud?
”"""

messages = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("{question}")
]
prompt = ChatPromptTemplate.from_messages(messages)

chain_type_kwargs = {"prompt": prompt}
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7, max_tokens=256)  # Modify model_name if you have access to GPT-4
chain = RetrievalQAWithSourcesChain.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vector_store.as_retriever(),
    return_source_documents=True,
    chain_type_kwargs=chain_type_kwargs
)

with st.spinner("Thinking..."):
    query = st.text_input("Question for the book?", value="What is the history or Wardley Mapping?")
    result = chain(query)
