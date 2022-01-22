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
    c = alt.Chart(df).transform_aggregate(
        sweet_mean='mean(甘辛度)',
        light_mean='mean(濃淡度)',
        groupby=['県名']
    ).mark_point(filled=True).encode(
        x=alt.X('sweet_mean:Q', axis=alt.Axis(title="←辛口  甘口→", grid=False)),
        y=alt.Y('light_mean:Q', axis=alt.Axis(title='←淡麗  濃醇→', grid=False)),
        tooltip=[
            alt.Tooltip('sweet_mean:Q', title='甘辛度'),
            alt.Tooltip('light_mean:Q', title='濃淡度'),
            '県名'],
    )


    text = c.mark_text(
        align='left',
        baseline='middle',
        dx=7
    ).encode(
        text='県名'
    )

    return c+text

def app():
    st.title("app")

    # load
    l = ds.Loader_CSV('./sake-gaikyo/rawdata/test_2020.csv')
    df = l.load()

    # filter1
    f1, f2 = st.columns(2)
    kinds = df["kind"].unique()
    years = df["year"].unique()
    kind = f1.multiselect("酒種", kinds, kinds)
    year = f2.multiselect("調査年", years, years)

    df = df[
        (df["kind"].isin(kind)) &
        (df["year"].isin(year))
    ]

    st.altair_chart(taste_plot(df), use_container_width=True)


    pref = df["県名"].unique()
    prefs = st.multiselect("都道府県", pref, pref)

    st.write("download")
    download_button(df)

if __name__ == '__main__':
    app()