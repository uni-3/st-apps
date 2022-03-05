import pandas as pd
import streamlit as st
import altair as alt

import pages.medical_practice as mp

import os

st.set_page_config(
    page_title="NDB viewer",
    page_icon=":hospital:",
    layout="wide",
    initial_sidebar_state="expanded",
)


def main():
    url_home = (
        "https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/0000177221_00008.html"
    )
    st.title("NDB open data viewer")
    st.markdown(f"datasource: [第５回NDBオープンデータ]({url_home})")

    pages = ["性年齢別", "都道府県別", "特定検診", "問診票"]
    page = st.sidebar.selectbox("表示ページ", pages, 0)

    if page == pages[0]:
        mp.page()
    elif page == pages[1]:
        pass
    elif page == pages[2]:
        pass
    elif page == pages[3]:
        pass


if __name__ == "__main__":
    main()