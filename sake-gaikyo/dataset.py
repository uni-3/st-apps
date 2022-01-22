import pandas as pd
import tabula

from abc import ABC, abstractmethod

# 2014は一般酒のみだったので除外
# 2015/16はカラム名が異なってるので除外
sources = [
    {
        "url": 'https://www.nta.go.jp/taxes/sake/shiori-gaikyo/seibun/2020/pdf/001.pdf',
        "pages": '35-38',
        "year": '2020',
    },
    {
        "url": "https://www.nta.go.jp/taxes/sake/shiori-gaikyo/seibun/2019/pdf/001.pdf",
        "pages": '36-39',
        "year": '2019',
    },
    {
        "url": "https://www.nta.go.jp/taxes/sake/shiori-gaikyo/seibun/2018/pdf/001.pdf",
        "pages": '36-39',
        "year": '2018',
    },
    {
        "url": "https://www.nta.go.jp/taxes/sake/shiori-gaikyo/seibun/2017/pdf/0417.pdf",
        "pages": '12-15',
        "year": '2017',
    },
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
                df_kind = self.format(df_kind)
                df_kind = df_kind.apply(pd.to_numeric, errors='ignore', downcast="float") # object -> float
                df_kind["year"] = s["year"]
                df_kind["kind"] = kinds[i]
                df = pd.concat([df, df_kind])
        return df

    def fetch(self, url, pages):
        return tabula.io.read_pdf(url, pages=pages, lattice=True)

    def format(self, df):
        # 2列目のrename
        df.rename(columns={'Unnamed: 0': '県名'}, inplace=True)

        # 集計行/複数県のデータがいるので削除
        df = df[df['県名'].notnull()]
        df = df[~df['県名'].str.contains("沖縄県")]
        df = df[~df['県名'].str.contains("局")]

        # セル内改行とスペース削除
        df.rename(columns=lambda s: ''.join(s.splitlines()), inplace=True)
        df.rename(columns=lambda s: s.replace(' ', ''), inplace=True)

        # 表と対応しない列削除
        drop_index_from = df.columns.get_loc("濃淡度")
        df.drop(df.columns[drop_index_from+1:].tolist(), axis=1, inplace=True)

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
    df.to_csv('./sake-gaikyo/rawdata/test_2020.csv', index=False)

if __name__ == '__main__':
    main()