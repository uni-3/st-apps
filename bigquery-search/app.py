
import asyncio
import streamlit as st
import pages.agent_page as ap
from google.oauth2 import service_account
from google.cloud import bigquery
from utils.inmemory_agent import call_agent_async, main

# Create API client.
if "credentials" in st.session_state:
    credentials = service_account.Credentials.from_service_account_info(st.session_state.credentials)
    client = bigquery.Client(credentials=credentials)
    st.write(f"Using credentials from session state. Project ID: {credentials.project_id}")
else:
    uploaded_file = st.file_uploader("Upload your GCP service account credentials", type=['json'])

    if uploaded_file is not None:
        credentials_info = uploaded_file.read()
        credentials = service_account.Credentials.from_service_account_info(credentials_info)
        client = bigquery.Client(credentials=credentials)

        # Save credentials to st.session_state
        st.session_state.credentials = credentials_info
        st.success("Credentials uploaded and saved to session state!")
    else:
        st.warning("Please upload your GCP service account credentials.")
        st.stop()

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows

rows = run_query("SELECT word FROM `bigquery-public-data.samples.shakespeare` LIMIT 10")

# Print results.
st.write("Some wise words from Shakespeare:")
for row in rows:
    st.write("✍️ " + row['word'])

st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", ["Home", "Agent"])

if page == "Home":
    st.write("Welcome to the home page!")
elif page == "Agent":
    ap.page()
