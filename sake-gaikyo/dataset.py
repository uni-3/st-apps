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


def main():
    for s in sources:
        dfs = load_data(s["url"], s["pages"])

        for i, df in enumerate(dfs):
            print(df)
            df.to_csv(f'{kinds[i]}{s["filename"]}')

if __name__ == '__main__':
    main()