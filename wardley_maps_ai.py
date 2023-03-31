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

def get_text():
    input_text = st.text_input(label="Question ",  placeholder="How many components are in this map?", key="q_input")
    return input_text

    q_input = get_text()
    
if len(q_input.split(" ")) > 700:
    st.write("Please enter a shorter question about your Wardley Map")
st.stop()
                                                           
st.button("*See An Example*", type='secondary', help="Click to see an example.", on_click=update_text_with_example)
                                                           
def update_text_with_example():
    print ("in updated")
    st.session_state.email_input = "How many components are in this map?"
    
st.markdown("### Response:")

llm = load_LLM(["OPENAI_API_KEY"])

prompt_with_email = prompt.format(question=question, map=map)

formatted_email = llm(prompt_with_email)

    st.write(formatted_email)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("After a tweet thread on prompt engineering using Wardley Maps \n\n This tool \
        was created to load your Wardley Maps and ask questions about it using AI. This tool \
        is powered by [LangChain](https://langchain.com/) and [OpenAI](https://openai.com) and made by \
        [@mcraddock](https://twitter.com/mcraddock). \n\n View Source Code on [Github](https://github.com/tractorjuice/globalize-text-streamlit2/edit/main/main.py)")

        st.markdown("## Enter your Wardley Map")
        
    with col2:
        st.image(image='prompt-engineering-wardley.png', width=500, caption='https://twitter.com/mcraddock/status/1641537955507347476')

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
        else:
            st.error("Map not found. Please enter a valid ID.")
            
            
            
            
            

if __name__ == "__main__":
    app()
