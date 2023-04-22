import streamlit as st
import requests

st.set_page_config(page_title="Intro To Wardley Mapping with AI")
st.title("Intro To Wardley Mapping with AI")
st.sidebar.markdown("# Query this video using AI")

st.sidebar.markdown("Developed by Mark Craddock](https://twitter.com/mcraddock)", unsafe_allow_html=True)
st.sidebar.markdown("Current Version: 0.0.2")

# Replace with your desired API URL
api_url = "https://firstliot.steamship.run/wardleymapsbok-1c4/wardleymapsbok-1c4/qa"

prompt = st.text_input("Prompt", value="What is this video about?")

# Set your query parameters
query_params = {
    "query": "What is inertia?"
}


text = st.empty()

if st.button("Send"):
    with st.spinner("Generating response..."):
        
        # Send the GET request with query parameters
        response = requests.get(api_url, params=query_params)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Process the JSON data
            data = response.json()
            st.video('https://youtu.be/KkePAhnkHeg') 
            st.write(data)
        else:
            print(f"API request failed with status code: {response.status_code}")
            st.json(response)
            text.text_area("Messages", response, height=250)

if st.button("Clear"):
    st.session_state["messages"] = BASE_PROMPT
    show_messages(text)
