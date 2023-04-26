import streamlit as st
from steamship import Steamship
import json

st.set_page_config(page_title="Ask SimonGPT")
st.title("Ask SimonGPT Anything")
st.sidebar.markdown("# Query this video using AI")
st.sidebar.markdown("Developed by Mark Craddock](https://twitter.com/mcraddock)", unsafe_allow_html=True)
st.sidebar.markdown("Current Version: 0.0.2")
st.sidebar.markdown("1M+ Vectors")

    
# Load the package instance stub.
pkg = Steamship.use(
    "wardleymapsbok",
    instance_handle="wardleymapsbok-e2j",
    api_key = st.secrets["STEAMSHIP_API_KEY"]
)


with st.form(key='query_form'):
    prompt = st.text_input("Question", value="What is inertia?")
    submit_button = st.form_submit_button(label='Send')

if submit_button:
    with st.spinner("Generating response..."):
        # Invoke the method
        response = pkg.invoke(
            "qa",
            query=prompt
        )

        # Parse the JSON response
        response_json = json.loads(response)

        # Display answer
        answer = response_json["answer"]
        st.write(f"**Answer:** {answer}")
        st.write("Relevant content should start within 10 seconds from the videos below")

        for i in range(len(response_json['source_urls'])):
            source_container = st.container()
            with source_container:
                st.write(f"Source {i+1}:")
                if 'source_title' in response_json and len(response_json['source_title']) > i:
                    st.write("**Title:**", response_json['source_title'][i])
                if 'source_author' in response_json and len(response_json['source_author']) > i:
                    st.write("**Author:**", response_json['source_author'][i])
                if 'source_urls' in response_json and len(response_json['source_urls']) > i:
                    st.write("**URL:**", f"https://www.youtube.com/watch?v={response_json['source_urls'][i]}")
                if 'source_description' in response_json and len(response_json['source_description']) > i:
                    st.write("**Description:**", response_json['source_description'][i])
                st.write("")


        
if st.button("Clear"):
    st.session_state["messages"] = BASE_PROMPT
    show_messages(text)
