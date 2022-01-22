import streamlit as st
import altair as alt
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

def taste_plot(df):
    """
    light/full: 淡麗、濃醇
    sweet/dry: 甘口、辛口
    甘辛度,濃淡度,
    """
    c = alt.Chart(df).mark_point(filled=True).encode(
        x=alt.X('mean(甘辛度)', axis=alt.Axis(title='甘辛度')),
        y=alt.Y('mean(濃淡度)', axis=alt.Axis(title='濃淡度')),
        tooltip=['甘辛度', '濃淡度', '都道府県']
    )

    text = c.mark_text(
        align='left',
        baseline='middle',
        dx=7
    ).encode(
        text='都道府県'
    )

    return c+text

def app():
    st.title("app")

    # load
    l = ds.Loader_CSV('./sake-gaikyo/rawdata/test_2020.csv')
    df = l.load()

    #
    kind = st.multiselect("酒種", df["kind"])
    year = st.multiselect("年", df["year"].unique())

    st.altair_chart(taste_plot(df), use_container_width=True)


    prefs = st.multiselect("都道府県", df["県名"].unique())

    st.write("download")
    download_button(df)

if __name__ == '__main__':
    app()