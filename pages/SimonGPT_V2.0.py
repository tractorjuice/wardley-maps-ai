import streamlit as st
from steamship import Steamship
import json

st.set_page_config(page_title="Ask SimonGPT")
st.title("Ask SimonGPT Anything")
st.sidebar.markdown("# Query this video using AI")
st.sidebar.markdown("Developed by Mark Craddock](https://twitter.com/mcraddock)", unsafe_allow_html=True)
st.sidebar.markdown("Current Version: 0.0.2")
    
# Load the package instance stub.
pkg = Steamship.use(
    "wardleymapsbok",
    instance_handle="wardleymapsbok-1c4",
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
        st.write("Relevant content should start within 30 seconds from the videos below")
        for i in range(len(response_json['source_urls'])):
            st.write(f"Source {i+1}:")
            #st.markdown(f"**Title:** {response_json['source_title'][i]}")
            if 'source_author' in response_json:
                st.markdown(f"**Author:** {data['source_author'][i]}")
            #st.markdown(f"**URL:** {response_json['source_urls'][i]}")
            #st.write("")
            
            
for i in range(len(data['source_urls'])):
    st.write(f"Source {i+1}:")
    st.markdown(f"**Title:** {data['source_title'][i]}")
    if 'source_author' in data:
        st.markdown(f"**Author:** {data['source_author'][i]}")
    st.markdown(f"**URL:** {data['source_urls'][i]}")
    st.write("")

        # Display source URLs
        #st.write("**Source URLs:**")
        #source_urls_list = response_json["source_urls"]
        #for index, url in enumerate(source_urls_list):
        #    st.write(f"{index + 1}. [{url}]({url})")
        
if st.button("Clear"):
    st.session_state["messages"] = BASE_PROMPT
    show_messages(text)
