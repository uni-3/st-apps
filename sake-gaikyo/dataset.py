import pandas as pd
import tabula

from abc import ABC, abstractmethod

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

class Loader(ABC):
    @abstractmethod
    def load(self) -> pd.DataFrame:
        pass


class Loader_PDF(Loader):
    def __init__(self, sources):
        self.sources = sources

    def load(self):
        df = pd.DataFrame()
        for s in self.sources:
            for i, df_kind in enumerate(self.fetch(s["url"], s["pages"])):
                df_kind = self.format_df(df_kind)
                df_kind["year"] = s["year"]
                df_kind["kind"] = kinds[i]
                df = pd.concat([df, df_kind])

    def fetch(self, url, pages):
        return tabula.io.read_pdf(url, pages=pages, lattice=True)

    def format_df(self, df):
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

class Loader_CSV(Loader):
    def __init__(self, path):
        self.path = path

    def load(self):
        return pd.read_csv(self.path)


def main():
    l = Loader_PDF(sources)
    df = l.load()

if __name__ == '__main__':
    main()