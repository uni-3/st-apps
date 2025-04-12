import streamlit as st
from utils.inmemory_agent import agent
import asyncio
import streamlit as st

st.title("In-Memory Agent Page")

google_api_key = st.text_input("Enter your Google API Key:", type="password")

query = st.text_input("Enter your query:")
if st.button("Submit") and google_api_key:
    import os
    os.environ["GOOGLE_API_KEY"] = google_api_key
    st.success("Google API Key set successfully!")
    if query:
        try:
            res = asyncio.run(agent(query))
            st.write("Response:", res)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a query.")
    #st.warning("Please enter a query.")
