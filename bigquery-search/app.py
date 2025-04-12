
import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery

# Create API client.
uploaded_file = st.file_uploader("Upload your GCP service account credentials", type=['json'])

if uploaded_file is not None:
    credentials_info = uploaded_file.read()
    credentials = service_account.Credentials.from_service_account_info(credentials_info)
    client = bigquery.Client(credentials=credentials)
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
