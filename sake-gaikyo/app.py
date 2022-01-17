import streamlit as st
import pandas as pd

import dataset as ds

@st.cache
def load_data():
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
    df = load_data()
    st.subheader("download")
    download_button(df)


if __name__ == '__main__':
    app()