import streamlit as st
import requests
import re
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
	ChatPromptTemplate,
	SystemMessagePromptTemplate,
	AIMessagePromptTemplate,
	HumanMessagePromptTemplate,
)
import llama_index
from llama_index import LLMPredictor, GPTSimpleVectorIndex, PromptHelper
import os
from pathlib import Path
from gpt_index import download_loader
from langchain.schema import (
	AIMessage,
	HumanMessage,
	SystemMessage
)

API_ENDPOINT = "https://api.onlinewardleymaps.com/v1/maps/fetch?id="
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# Set the page title and layout
st.set_page_config(page_title="Chat with your map")
st.title("Chat with your map")
st.sidebar.markdown("# Ask Questions about Your Map")
st.sidebar.markdown("Developed by Mark Craddock](https://twitter.com/mcraddock)", unsafe_allow_html=True)
st.sidebar.markdown("Current Version: 0.0.2")

template = """
 Write a review of the Wardley Map on {title} below, focusing on its accuracy in representing the needs and goals of the user, assessing its usefulness for decision-making, and analyzing its limitations and potential for improvement.

Suggestions:

Provide a brief overview of the Wardley Map for {title}, including the components and relationships it represents.
Describe how the map captures the needs and goals of the user, and assess its accuracy in representing these aspects.
Discuss the usefulness of the map for decision-making related to {title}, with a focus on how it informs decisions about user needs and goals.
Analyze the limitations of the map, such as any missing or incomplete components, and suggest potential improvements to enhance its accuracy and usefulness for user-focused decision-making.

QUESTION: {question}
WARDLEY MAP: {map}

YOUR RESPONSE:
"""

BASE_PROMPT = [{"role": "system", "content": "You are a helpful assistant."}]

if "messages" not in st.session_state:
	st.session_state["messages"] = BASE_PROMPT

def load_LLM(openai_api_key):
	"""Logic for loading the chain you want to use should go here."""
	llm = OpenAI(temperature=0.7, openai_api_key=OPENAI_API_KEY, max_tokens=500)
	return llm

def show_messages(text):
	messages_str = [
		f"{_['role']}: {_['content']}" for _ in st.session_state["messages"][1:]
	]
	st.write (messages_str)
	text.text_area("Messages", value=str("\n".join(messages_str)), height=300)

# Define the form to enter the map ID
map_id = st.text_input("Enter the ID of the Wardley Map: For example https://onlinewardleymaps.com/#clone:OXeRWhqHSLDXfOnrfI, enter: OXeRWhqHSLDXfOnrfI", value="OXeRWhqHSLDXfOnrfI")

# Load the map data when the user submits the form
if st.button("Load Map"):
		with st.spinner("Generating response..."):
			# Fetch the map data from the API
			url = f"https://api.onlinewardleymaps.com/v1/maps/fetch?id={map_id}"
			response = requests.get(url)
			
			# Check if the map was found
			if response.status_code == 200:
				map_data = response.json()
				st.session_state.map_data=map_data
				#st.write ("#Wardley Map")
				st.write (st.session_state.map_data)
				
				map_data_str = map_data['text'].split("/n")
				st.session_state.map_data_str=map_data_str
				
				for line in map_data_str:
					x_y = re.findall("\[(.*?)\]", line)
					if x_y:
						#st.write (x_y)
						match = x_y[0]
						match = match.split(sep = ",")
						match = match[::-1]
						
						new_xy = ('[' + match[0].strip() + ',' + match[1] + ']')
						new_line = re.sub("\[(.*?)\]", new_xy, line, count = 1)
						
						st.write (new_line)
						#new_map_data'text'].append(newline)
					else:
						#new_map_data['text'].append(line)
						st.write (line)
				
				#Debug
				#st.write ("#New Wardley Map")
				#st.write (new_map_data)
				
			else:
				st.error("Map not found. Please enter a valid ID.")

text = st.empty()
show_messages(text)

question = st.text_input("Prompt", value="What is this Wardley Map about?")

prompt = PromptTemplate(
	input_variables=["title", "question","map"],
	template=template,
)

llm = load_LLM(OPENAI_API_KEY)

#st.write (st.session_state.map_data)

if st.button("Send"):
	with st.spinner("Generating response..."):
		
		prompt_wardley_ai = prompt.format(question=question, map=st.session_state.map_data_str)
		response = llm(prompt_wardley_ai)		
		text.text_area("Messages", response, height=250)

if st.button("Clear"):
    st.session_state["messages"] = BASE_PROMPT
    show_messages(text)
