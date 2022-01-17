import streamlit as st
import pandas as pd

import dataset as ds

@st.cache
def load_data(loader: ds.Loader):
    return ds.load()


def download_button(df):
    csv = df.to_csv(index=False).encode('utf-8')

    st.download_button(
        "Download as CSV",
        csv,
        "export.csv",
        "text/csv",
        key='download-csv'
    )


def app():
    st.title("app")

    # load
    l = ds.Loader_CSV('./sake-gaikyo/rawdata/test_2020.csv')
    df = l.load()
    st.subheader("download")
    download_button(df)


if __name__ == '__main__':
    app()