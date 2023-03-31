import streamlit as st
import requests
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

API_ENDPOINT = "https://api.onlinewardleymaps.com/v1/maps/fetch?id="

template = """
    Your goal is to:
    - Answer the question below about the map below.

    Below is the map and question:
    MAP: {map}
    QUESTION: {question}
    
    YOUR RESPONSE:
"""

# Define the Streamlit app
def app():

    # Set the page title and layout
    st.set_page_config(page_title="Wardley Maps with AI")
    st.title("Wardley Maps with AI")
        
    # Define the form to enter the map ID
    map_id = st.text_input("Enter the ID of the Wardley Map")
    question = st.text_input(label="Question ", placeholder="How many components are in this map?", key="q_input")
    if len(question.split(" ")) > 700:
        st.write("Please enter a shorter question about your Wardley Map")
        st.stop()

    # Load the map data when the user submits the form
    if st.button("Load Map"):
        # Fetch the map data from the API
        url = f"https://api.onlinewardleymaps.com/v1/maps/fetch?id={map_id}"
        response = requests.get(url)

        # Check if the map was found
        if response.status_code == 200:
            map_data = response.json()

            # Display the map
            #st.write(map_data)
            
            prompt = PromptTemplate(
                input_variables=["map", "question"],
                template=template,
            )
            
            st.markdown("### Prompt:")
            st.write(prompt)
            
            def load_LLM(openai_api_key):
                """Logic for loading the chain you want to use should go here."""
                llm = OpenAI(temperature=0, openai_api_key=st.secrets["OPENAI_API_KEY"],model_name="gpt-4")
                return llm
            
            llm = load_LLM(["OPENAI_API_KEY"])
            
            prompt_wardley_ai = prompt.format(question=question, map=map_data)
            response = llm(prompt_wardley_ai)
            
            #st.markdown("### Input Prompt:")
            #st.write(prompt_wardley_ai)
            
            #st.markdown("### Question:")
            #st.write(question)
            
            st.markdown("### Response:")
            st.write(response)
                   
        else:
            st.error("Map not found. Please enter a valid ID.")
                                                                                                                          
if __name__ == "__main__":
    app()
