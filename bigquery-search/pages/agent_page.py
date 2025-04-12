import streamlit as st
from utils.inmemory_agent import agent
import asyncio
import streamlit as st

st.title("In-Memory Agent Page")

google_api_key = st.text_input("Enter your Google API Key:", type="password")

with st.form(key='my_form'):
    query = st.text_input("Enter your query:")
    submitted = st.form_submit_button("Submit")

if submitted and google_api_key:
    import os
    os.environ["GOOGLE_API_KEY"] = google_api_key
    #st.success("Google API Key set successfully!")
    if query:
        try:
            res = asyncio.run(agent(query))
            st.write("Response:", res)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a query.")
