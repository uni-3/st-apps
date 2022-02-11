import streamlit as st
import altair as alt
import pandas as pd
import dataset as ds
import matplotlib.pyplot as plt


@st.cache
def load_data(loader: ds.Loader):
    return loader.load()


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
            alt.Tooltip('sweet_mean:Q', title='甘辛度', format=".2f"),
            alt.Tooltip('light_mean:Q', title='濃淡度', format=".2f"),
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


def timeseries_plot(df, v):
    c = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X('year:O', axis=alt.Axis(title='調査年', grid=False)),
        y=alt.Y(f'mean({v}):Q', axis=alt.Axis(title=v, grid=False)),
        tooltip=[
            alt.Tooltip(f'mean({v}):Q', title=v, format=".2f"),
        ],
        color=alt.Color("kind:N", title="酒種")
    )
    text = c.mark_text(
        align='center',
        baseline='middle',
        dx=5,
        dy=10
    ).encode(
        text=alt.Text(f'mean({v}):Q', format=".2f")
    )

    return c+text


def corr_plot(df, values):
    h = alt.Chart(df).mark_rect().encode(
        x=alt.X(values),
        y=alt.Y(values)
    )

    return h


def map_plot(df, value_col):
    """
    https://docs.streamlit.io/library/api-reference/charts/st.pydeck_chart
    """

    regions = alt.topo_feature(
        'https://raw.githubusercontent.com/dataofjapan/land/master/japan.topojson', 'japan')

    map = alt.Chart(regions).mark_geoshape(
        stroke='black',
        strokeWidth=0.1
    ).transform_lookup(
        lookup='properties.nam_ja',
        from_=alt.LookupData(df, '県名', [value_col])
    ).encode(
        tooltip=[
            alt.Tooltip('properties.nam_ja:N', title='県名'),
            alt.Tooltip(f'{value_col}:Q', format='.2f')
        ],
        color=f'{value_col}:Q',
    )

    return map


def app():
    st.title("全国市販酒類調査 - 全国の清酒成分比較 -")

    # load
    # l = ds.Loader_CSV('./sake-gaikyo/rawdata/test_2020.csv')
    data_load_state = st.text('データ取得中...')
    l = ds.Loader_PDF(ds.sources)
    df_raw = load_data(l)
    data_load_state.text('')
    value_cols = ["アルコール分", "日本酒度", "エキス分", "酸度", "アミノ酸度", "甘辛度", "濃淡度"]


    # filter1
    st.subheader("都道府県ごとの特徴")
    df = df_raw.copy()
    f1, f2 = st.columns(2)
    kinds = df["kind"].unique()
    years = df["year"].unique()
    kind = f1.multiselect("酒類", kinds, kinds)
    year = f2.multiselect("調査年", years, years)

    # taste
    df = df[
        (df["kind"].isin(kind)) &
        (df["year"].isin(year))
    ]
    st.altair_chart(taste_plot(df), use_container_width=True)

    # map
    m_value = st.selectbox("値", value_cols)
    st.altair_chart(map_plot(df, m_value), use_container_width=True)

    # time series
    st.subheader("経年変化")
    df = df_raw.copy()
    f3, f4 = st.columns(2)
    kinds = df["kind"].unique()
    value = f3.selectbox("", value_cols)
    kind = f4.multiselect("", kinds, kinds)

    df = df[
        (df["kind"].isin(kind))
    ]
    st.altair_chart(timeseries_plot(df, value), use_container_width=True)

    # corr
    st.subheader("各値の相関")
    st.markdown("**エキス分、甘辛度、濃淡度は他の数値から算出されるため除外している**")
    df = df_raw.copy()
    raw_value_cols = ["アルコール分", "日本酒度", "酸度", "アミノ酸度"]
    df_corr = df[raw_value_cols].corr()
    with pd.option_context('precision', 3):
        st.dataframe(df_corr.style.background_gradient(axis=None), 500, 400)

    # pref = df["県名"].unique()
    # prefs = st.multiselect("都道府県", pref, pref)

    st.subheader("download")
    download_button(df)
    st.write("source: https://www.nta.go.jp/taxes/sake/shiori-gaikyo/seibun/06.htm")


if __name__ == '__main__':
    app()
