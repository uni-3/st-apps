import pandas as pd
import tabula

sources = [
    {
        "url": 'https://www.nta.go.jp/taxes/sake/shiori-gaikyo/seibun/2020/pdf/001.pdf',
        "pages": '35-38',
        "filename": '_gaiyou_2020.csv',
    }
]
kinds = ['一般酒', '吟醸酒', '純米酒', '本醸造酒']

def load_data(url, pages):
    return tabula.io.read_pdf(url, pages=pages, lattice=True)


def format_df(df):
    # 2列目のrename
    df.rename(columns={'Unnamed: 0': '県名'}, inplace=True)

    # 集計行が間にいるので削除
    df = df[df['県名'].notnull()]

    # 表と対応しない列削除
    drop_index_from = df.columns.get_loc("Unnamed: 1")
    df.drop(df.columns[drop_index_from:].tolist(), axis=1, inplace=True)

    # セル内改行
    df.rename(columns=lambda s: ''.join(s.splitlines()), inplace=True)
    return df

def main():
    for s in sources:
        dfs = load_data(s["url"], s["pages"])

        for i, df in enumerate(dfs):
            df = format_df(df)
            df.to_csv(f'{kinds[i]}{s["filename"]}')


if __name__ == '__main__':
    main()