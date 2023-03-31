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

prompt = PromptTemplate(
    input_variables=["map", "question"],
    template=template,
)

def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=st.secrets["OPENAI_API_KEY"])
    return llm

# Define the Streamlit app
def app():

    # Set the page title and layout
    st.set_page_config(page_title="Wardley Maps with AI")
    st.title("Wardley Maps with AI")
    
    q_input = st.text_input(label="Question ", placeholder="How many components are in this map?", key="q_input")
    
    if len(q_input.split(" ")) > 700:
        st.write("Please enter a shorter question about your Wardley Map")
    st.stop()
    
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
            
                st.session_state.email_input = "How many components are in this map?"
    
                st.markdown("### Response:")

                llm = load_LLM(["OPENAI_API_KEY"])

                prompt_with_email = prompt.format(question=question, map=map)
                formatted_email = llm(prompt_with_email)
                st.write(formatted_email)
                   
        else:
            st.error("Map not found. Please enter a valid ID.")
                                                                                                                          
if __name__ == "__main__":
    app()
