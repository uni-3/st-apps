import pandas as pd
import streamlit as st
from google.cloud import bigquery

projectId = st.secrets["gcp_project"]


@st.cache_resource()
def bq():
    client = bigquery.Client(projectId)
    return client


@st.cache_data(ttl=60 * 10, show_spinner=False)
def query(sql: str) -> pd.DataFrame:
    return bq().query(sql).to_dataframe()
