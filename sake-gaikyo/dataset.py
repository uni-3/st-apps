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
    return tabula.read_pdf(url, pages=pages, lattice=True)


def format_df(df):
    # セル内改行
    df.rename(columns=lambda s: ''.join(s.splitlines()), inplace=True)

    # 1列目、2列目のrename
    df.rename(columns={'Unnamed: 0': '県名'}, inplace=True)

    return df

def main():
    for s in sources:
        dfs = load_data(s["url"], s["pages"])

        for i, df in enumerate(dfs):
            df = format_df(df)
            print(df.columns)
            df.to_csv(f'{kinds[i]}{s["filename"]}')

if __name__ == '__main__':
    main()