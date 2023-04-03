import streamlit as st

st.set_page_config(
    page_title="Wardley Mapping with AI",
)

st.write("# Welcome to Wardley Mapping with AI")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    Streamlit is an open-source app framework built specifically for
    Machine Learning and Data Science projects.
    **Select a demo from the sidebar** to see some examples
    of what Streamlit can do!
    ### Want to learn more?
    - Check out [Twitter thread](https://twitter.com/mcraddock/status/1641537955507347476)
"""
)
