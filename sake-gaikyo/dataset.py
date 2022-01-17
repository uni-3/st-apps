import pandas as pd
import tabula

sources = [
    {
        "url": 'https://www.nta.go.jp/taxes/sake/shiori-gaikyo/seibun/2020/pdf/001.pdf',
        "pages": '35-38',
        "year": '2020',
    }
]

# TODO: parse from tables title 
# https://stackoverflow.com/questions/58185404/python-pdf-parsing-with-camelot-and-extract-the-table-title
kinds = ['一般酒', '吟醸酒', '純米酒', '本醸造酒']

def load():
    df = pd.DataFrame()
    for s in sources:
        for i, df_kind in enumerate(fetch(s["url"], s["pages"])):
            df_kind = format_df(df_kind)
            df_kind["year"] = s["year"]
            df_kind["kind"] = kinds[i]
            df = pd.concat([df, df_kind])

    return df

def fetch(url, pages):
    return tabula.io.read_pdf(url, pages=pages, lattice=True)


def format_df(df):
    # 2列目のrename
    df.rename(columns={'Unnamed: 0': '県名'}, inplace=True)

    # 集計行がいるので削除
    df = df[df['県名'].notnull()]

    # 表と対応しない列削除
    drop_index_from = df.columns.get_loc("Unnamed: 1")
    df.drop(df.columns[drop_index_from:].tolist(), axis=1, inplace=True)

    # セル内改行とスペース削除
    df.rename(columns=lambda s: ''.join(s.splitlines()), inplace=True)
    df.rename(columns=lambda s: s.replace(' ', ''), inplace=True)

    # 特定のデータにしか無い列削除
    df.drop(
        ["酢酸イソアミル(mg/L)", "カプロン酸エチル(mg/L)"], axis=1, inplace=True, errors='ignore')

    return df

def main():
    for s in sources:
        dfs = fetch(s["url"], s["pages"])

        for i, df in enumerate(dfs):
            df = format_df(df)
            df.to_csv(f'{kinds[i]}_{s["year"]}_gaiyou.csv', index=False)


if __name__ == '__main__':
    main()