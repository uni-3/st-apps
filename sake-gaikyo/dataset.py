import pandas as pd
import tabula


url = 'https://www.nta.go.jp/taxes/sake/shiori-gaikyo/seibun/2020/pdf/001.pdf'


def main():
    df = tabula.read_pdf(url)
    print(df)

if __name__ == '__main__':
    main()