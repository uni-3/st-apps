urls = [
    "https://www.mhlw.go.jp/content/12400000/000539815.xlsx",
    "https://www.mhlw.go.jp/content/12400000/000539816.xlsx",
    "https://www.mhlw.go.jp/content/12400000/000539817.xlsx",
    "https://www.mhlw.go.jp/content/12400000/000539818.xlsx",
    "https://www.mhlw.go.jp/content/12400000/000539820.xlsx",
    "https://www.mhlw.go.jp/content/12400000/000539821.xlsx",
    "https://www.mhlw.go.jp/content/12400000/000539822.xlsx",
    "https://www.mhlw.go.jp/content/12400000/000539823.xlsx",
    "https://www.mhlw.go.jp/content/12400000/000539824.xlsx",
    "https://www.mhlw.go.jp/content/12400000/000539825.xlsx",
    "https://www.mhlw.go.jp/content/12400000/000539826.xlsx",
    "https://www.mhlw.go.jp/content/12400000/000539827.xlsx",
    "https://www.mhlw.go.jp/content/12400000/000711554.xlsx",
    "https://www.mhlw.go.jp/content/12400000/000539829.xlsx",
    "https://www.mhlw.go.jp/content/12400000/000539830.xlsx",
    "https://www.mhlw.go.jp/content/12400000/000539831.xlsx",
    "https://www.mhlw.go.jp/content/12400000/000539832.xlsx",
    "https://www.mhlw.go.jp/content/12400000/000539833.xlsx",
    "https://www.mhlw.go.jp/content/12400000/000539834.xlsx",
    "https://www.mhlw.go.jp/content/12400000/000539835.xlsx",
    "https://www.mhlw.go.jp/content/12400000/000539836.xlsx",
    "https://www.mhlw.go.jp/content/12400000/000539837.xlsx",
    "https://www.mhlw.go.jp/content/12400000/000539838.xlsx",
    "https://www.mhlw.go.jp/content/12400000/000539839.xlsx",
    "https://www.mhlw.go.jp/content/12400000/000539840.xlsx",
]

titles = [
    "BMI 都道府県別性年齢階級別分布",
    "GOT（AST） 都道府県別性年齢階級別分布",
    "GPT（ALT） 都道府県別性年齢階級別分布",
    "HbA1c 都道府県別性年齢階級別分布",
    "HDLコレステロール 都道府県別性年齢階級別分布",
    "LDLコレステロール 都道府県別性年齢階級別分布",
    "γ-GT（γ-GTP） 都道府県別性年齢階級別分布",
    "ヘモグロビン 都道府県別性年齢階級別分布",
    "各項目の平均値 都道府県別性年齢階級別分布",
    "拡張期血圧 都道府県別性年齢階級別分布",
    "眼底検査（SCOTT分類) 都道府県別性年齢階級別分布",
    "眼底検査（キースワグナー分類） 都道府県別性年齢階級別分布",
    "眼底検査（シェイエ分類：H） 都道府県別性年齢階級別分布",
    "眼底検査（シェイエ分類：S） 都道府県別性年齢階級別分布",
    "空腹時血糖 都道府県別性年齢階級別分布",
    "収縮期血圧 都道府県別性年齢階級別分布",
    "中性脂肪 都道府県別性年齢階級別分布",
    "尿蛋白 都道府県別性年齢階級別分布",
    "尿糖 都道府県別性年齢階級別分布",
    "腹囲 都道府県別性年齢階級別分布",
    "ヘモグロビン 都道府県別性年齢階級別分布",
    "眼底検査（SCOTT分類) 都道府県別性年齢階級別分布",
    "眼底検査（キースワグナー分類） 都道府県別性年齢階級別分布",
    "眼底検査（シェイエ分類：H） 都道府県別性年齢階級別分布",
    "眼底検査（シェイエ分類：S） 都道府県別性年齢階級別分布",
]

# https://stackoverflow.com/questions/14507794/pandas-how-to-flatten-a-hierarchical-index-in-columns
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.MultiIndex.to_flat_index.html


def page():
    df_data = pd.DataFrame({"kind": titles, "url": urls})
    iter_csv = pd.read_csv("../dataset/urls.csv", iterator=True, chunksize=100)
    df_data = pd.concat(
        [chunk[chunk["title"].str.contains("都道府県")] for chunk in iter_csv]
    )

    kind = st.sidebar.selectbox("データセット名", df_data["kind"].tolist())

    url = df_data[df_data["kind"] == kind]["url"].tolist()[0]
