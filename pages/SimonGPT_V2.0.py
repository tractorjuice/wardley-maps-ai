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
    instance_handle="wardleymapsbok-3fe",
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
        st.write("Relevant content should start within 10 seconds from the videos below")

        num_sources = len(response_json['source_urls'])
        num_cols = 2
        num_rows = (num_sources + num_cols - 1) // num_cols

        sources = [
            {
                "title": response_json['source_title'][i],
                "author": response_json['source_author'][i],
                "url": f"https://www.youtube.com/watch?v={response_json['source_urls'][i]}",
                "description": response_json['source_description'][i]
            }
            for i in range(num_sources)
        ]

        # Split sources into two columns
        cols = st.beta_columns(num_cols)
        for i, col in enumerate(cols):
            for j in range(num_rows):
                source_index = j * num_cols + i
                if source_index < num_sources:
                    source = sources[source_index]
                    col.write(f"Source {source_index+1}:")
                    col.write("**Title:**", source["title"])
                    col.write("**Author:**", source["author"])
                    col.write("**URL:**", source["url"])
                    col.write("**Description:**", source["description"])
                    col.write("")


        
if st.button("Clear"):
    st.session_state["messages"] = BASE_PROMPT
    show_messages(text)
