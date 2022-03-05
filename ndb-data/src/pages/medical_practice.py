import streamlit as st
import pandas as pd
import altair as alt

# 都道府県別
# "https://www.mhlw.go.jp/content/12400000/000539712.xlsx",
# "精神科専門療法性都道府県",


def selects(df, col_name, suffix=""):
    # defaultは全選択
    val = st.sidebar.multiselect(
        col_name + suffix,
        df[col_name].unique().tolist(),
        df[col_name].unique().tolist(),
    )

    return val


def select(df, col_name, suffix=""):
    # defaultは一個
    val = st.sidebar.selectbox(
        col_name + suffix,
        df[col_name].unique().tolist(),
        0
        # df[col_name].unique().tolist()[0],
    )

    return val


# @st.cache
def load_data(url):
    df_raw = pd.read_excel(url, skiprows=[0], header=[1, 2])
    df_raw = df_raw.fillna(method="ffill")
    df_raw = df_raw.fillna(method="ffill", axis=1)
    return df_raw


def page():
    iter_csv = pd.read_csv("./dataset/urls.csv", iterator=True, chunksize=100)
    df_data = pd.concat(
        [chunk[chunk["title"].str.contains("性年齢")] for chunk in iter_csv]
    )

    title = st.sidebar.selectbox("データセット名", df_data["title"].tolist())

    url = df_data[df_data["title"] == title]["url"].tolist()[0]

    df_raw = load_data(url)

    # df_raw.columns = df_raw.iloc[0]
    # df_raw = df_raw.reindex(df_raw.index.drop(0))

    # d = pd.pivot_table(df_raw, index=["診療行為"])

    index_cols = []
    for col in df_raw.columns:
        if col[0] != "男" and col[0] != "女":
            index_cols.append(col[0])

    index_cols_1 = []
    for i in range(len(index_cols)):
        index_cols_1.append(f"Unnamed: {str(i)}_level_1")

    df = df_raw.melt(id_vars=index_cols, col_level=0, var_name="性別").join(
        df_raw.melt(id_vars=index_cols_1, col_level=1, var_name="年齢")["年齢"]
    )
    df["value"] = df["value"].replace("-", "0")

    # 選択（and選択）
    df_graph = df.copy()

    sex = selects(df_graph, "性別")
    kubun = select(df_graph, index_cols[1])
    df_graph = df_graph[
        (df_graph["性別"].isin(sex)) & (df_graph[index_cols[1]].isin([kubun]))
    ]

    nearest = alt.selection(
        type="single",
        nearest=True,
        on="mouseover",
        fields=["年齢"],
        empty="none",
    )
    scales = alt.selection_interval(bind="scales")

    line_plot = (
        alt.Chart(df_graph)
        .mark_line(point=True)
        .encode(
            x=alt.X("年齢:N", sort=None),
            y=alt.Y("value:Q", axis=alt.Axis(title="診療費")),
            color=index_cols[3] + ":N",
            tooltip=["年齢", index_cols[1], index_cols[3], "value"],
        )
    )

    selectors = (
        alt.Chart(df_graph)
        .mark_point()
        .encode(
            x=alt.X("年齢:N", sort=None),
            opacity=alt.value(0),
        )
        .add_selection(nearest)
    )
    points = line_plot.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )
    text = line_plot.mark_text(align="right", dx=5, dy=-5).encode(
        text=alt.condition(nearest, "value:Q", alt.value(" "))
    )
    st.altair_chart(
        alt.layer(line_plot, selectors, text)
        .add_selection(scales)
        .facet(row=alt.Row("性別:N"))
    )

    val_plot = (
        alt.Chart(df_graph)
        .mark_bar()
        .encode(
            x=alt.X("年齢:O", sort=None),
            y=alt.Y("sum(value):Q", axis=alt.Axis(title="診療費")),
            # x=alt.X("性別:N", sort=None, axis=alt.Axis(title=None, labels=False)),
            color="性別:N",
            # column="年齢:O",
            tooltip=["sum(value)"],
        )
    )
    st.altair_chart(val_plot)

    st.subheader("データセット")
    st.dataframe(df)