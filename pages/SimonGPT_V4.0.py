import streamlit as st
from steamship import Steamship
import json

st.set_page_config(page_title="Ask SimonGPT")
st.title("Ask SimonGPT Anything")
st.sidebar.markdown("# Query this video using AI")
st.sidebar.markdown("Developed by Mark Craddock](https://twitter.com/mcraddock)", unsafe_allow_html=True)
st.sidebar.markdown("Current Version: 0.0.4")
st.sidebar.markdown("Simon Wardley Content")
st.sidebar.markdown("1M+ Vectors")

# Load the package instance stub only if it has not been loaded before
if "pkg" not in st.session_state:
    # Load the package instance stub.
    st.session_state.pkg = Steamship.use(
        "simonbok",
        instance_handle="simonbok-210",
        api_key = st.secrets["STEAMSHIP_API_KEY"]
    )

with st.form(key='query_form'):
    prompt = st.text_input("Question", value="What is inertia?")
    submit_button = st.form_submit_button(label='Send')

if submit_button:
    with st.spinner("Generating response..."):
        # Invoke the method
        response = st.session_state.pkg.invoke(
            "qa",
            query=prompt
        )

        # Parse the JSON response
        response_json = json.loads(response)

        # Display answer
        answer = response_json["answer"]
        st.write(f"**Answer:** {answer}")

        # Split the output into two columns
        col1, col2 = st.columns(2)

        # First column
        with col1:
            st.write("Content from Simon Wardley")
            for i in range(len(response_json['source_urls'])):
                source_title = response_json.get('source_title', [''])[i].lower()
                source_container = st.container()
                with source_container:
                    st.write(f"Source {i+1}:")
                    if 'source_title' in response_json and len(response_json['source_title']) > i:
                        st.write("**Title:**", response_json['source_title'][i])
                    if 'source_author' in response_json and len(response_json['source_author']) > i:
                        st.write("**Author:**", response_json['source_author'][i])
                    if 'source_urls' in response_json and len(response_json['source_urls']) > i:
                        st.write("**URL:**", f"https://www.youtube.com/watch?feature=share&v={response_json['source_urls'][i]}")
                    if 'source_description' in response_json and len(response_json['source_description']) > i:
                        st.write("**Description:**", response_json['source_description'][i])
                    st.write("")

        # Second column
        with col2:
            for i in range(len(response_json['source_urls'])):
                if 'source_urls' in response_json and len(response_json['source_urls']) > i:
                    video_id = https://www.youtube.com/watch?feature=share&v={response_json['source_urls'][i]}
                    st.write(video_id)
                    st.video(video_id)
                
if st.button("Clear"):
    st.session_state["messages"] = BASE_PROMPT
    show_messages(text)
