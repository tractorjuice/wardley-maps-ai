import streamlit as st
import requests
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

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

    # Load the map data when the user submits the form
    if st.button("Load Map"):
        # Fetch the map data from the API
        url = f"https://api.onlinewardleymaps.com/v1/maps/fetch?id={map_id}"
        response = requests.get(url)

        # Check if the map was found
        if response.status_code == 200:
            map_data = response.json()

            # Display the map
            st.write(map_data)
            
            question = st.text_input(label="Question ", placeholder="How many components are in this map?", key="q_input")
            if len(question.split(" ")) > 700:
                st.write("Please enter a shorter question about your Wardley Map")
            st.stop()
            
            prompt = PromptTemplate(
                input_variables=["map", "question"],
                template=template,
            )
            
            st.write(prompt)

            def load_LLM(openai_api_key):
                """Logic for loading the chain you want to use should go here."""
                # Make sure your openai_api_key is set as an environment variable
                llm = OpenAI(temperature=.7, openai_api_key=st.secrets["OPENAI_API_KEY"])
                return llm
                
            st.markdown("### Response:")

            llm = load_LLM(["OPENAI_API_KEY"])

            prompt_wardley_ai = prompt.format(question=question, map=map_data)
            response = llm(prompt_wardley_ai)
            st.write(response)
            
            st.write(map_data)
                   
        else:
            st.error("Map not found. Please enter a valid ID.")
                                                                                                                          
if __name__ == "__main__":
    app()
