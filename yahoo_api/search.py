import streamlit as st
import pydeck as pdk
import pandas as pd
import requests

import json
from datetime import datetime

from authentication import check_password

API_KEY = st.secrets["yahoo_api_key"]
MAX_SHOW = 1000

# List of columns to drop
columns_to_drop = ["Geometry.Type",
                  "Geometry.Coordinates",
                   "Property.Uid",
                "Property.CassetteId", "Property.AddressMatchingLevel",
                "Property.ParkingFlag", "Property.SmartPhoneCouponFlag",
                "Property.Coupon", "Property.KeepCount"
                ]


class YahooLocalSearchAPI:
    """
    A class that interacts with the Yahoo Local Search API.

    Args:
        api_key (str): The API key for accessing the Yahoo Local Search API.

    Attributes:
        api_key (str): The API key for accessing the Yahoo Local Search API.
        base_url (str): The base URL for the Yahoo Local Search API.
        timeout (int): The timeout value for the API request.

    Methods:
        _build_params: Builds the parameters for the API request.
        search: Performs a search using the Yahoo Local Search API.
    """

    def __init__(self, api_key=API_KEY):
        self.api_key = api_key
        self.base_url = "https://map.yahooapis.jp/search/local/V1/localSearch"
        self.results = 100
        self.timeout = 1000

    def _build_params(self, query: str = None, start: int = 1):
        """
        Builds the parameters for the API request.

        Args:
            query (str): The search query.

        Returns:
            dict: The parameters for the API request.
        """
        params = {
            "appid": self.api_key,
            "query": query,
            "output": "json",
            "results": self.results,
            "start": start,
        }
        return params

    def search(self, query=None, start=1):
        """
        Performs a search using the Yahoo Local Search API.

        Args:
            query (str): The search query.

        Returns:
            dict: The JSON response from the API.
        """
        if not query:
            return None
        try:
            response = requests.get(self.base_url, timeout=self.timeout, params=self._build_params(query, start))
            response.raise_for_status()  # Raise an exception for non-2xx status codes
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred during the API request: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def search_all(self, query=None, threshhold=MAX_SHOW):
        all_data = []
        total = None
        start = 1
        progress_text = "loading..."
        progress_bar = st.progress(0, text=progress_text)

        while start is not None:
            res = self.search(query, start)
            if not res or 'Feature' not in res:
                break

            # 先に 1回だけ表示したい
            if total is None:
                st.write(f"Total: {res['ResultInfo']['Total']}")
            total = res["ResultInfo"]["Total"]
            if total == 0:
                break

            res_feature = res['Feature']
            all_data.extend(res_feature)
            start += len(res_feature)

            progress = min(start / total, 1.0)
            progress_bar.progress(progress, text=progress_text)

            if start > total or len(all_data) >= threshhold:
                break

        # 進捗バーを非表示に
        progress_bar.empty()

        return all_data, total

def parse_json_to_df(json_str: dict):
    # Step: Extract "Property" information from each "Feature" and convert it to pandas DataFrame
    #df = pd.json_normalize([feature['Property'] for feature in json_str['Feature']])
    #df = pd.json_normalize(json_str['Feature'])
    df = pd.json_normalize(json_str)

    df['lng'], df['lat'] = df['Geometry.Coordinates'].str.split(pat=',', n=1).str
    df['lat'] = df['lat'].astype(float)
    df['lng'] = df['lng'].astype(float)
    json_columns = ["Property.Genre", "Property.Station", "Property.Area"]
    for ac in json_columns:
        try:
            df[ac] = df[ac].apply(json.dumps, ensure_ascii=False)
        except KeyError:
            print(f"Column {ac} not found in the dataframe.")

    return df

# query
# uni coffee
# 050-3623-5328

def map_pydeck(df):
    layer = pdk.Layer(
        'ScatterplotLayer',
        data=df,
        get_position='[lng, lat]',
        get_radius=300,
        get_fill_color='[255, 160, 0, 100]',
        pickable=True
    )

    # Define the tooltip
    tooltip = {
        "html": "<b>Name:</b> {Name}<br/><b>Category:</b> {Category}<br/><b>Address:</b> {Property.Address}",
        "style": {
            "backgroundColor": "steelblue",
            "color": "white"
        }
    }

    # Create the map
    return pdk.Deck(
        initial_view_state=pdk.ViewState(
            latitude=df['lat'].mean(),
            longitude=df['lng'].mean(),
            zoom=10,
            pitch=0,
        ),
        layers=[layer],
        tooltip=tooltip
    )


def app():
    st.write("https://developer.yahoo.co.jp/webapi/map/openlocalplatform/v1/localsearch.html")
    y = YahooLocalSearchAPI()
    query = st.text_input("検索キーワード")
    print("query", query)
    if query:
        data, total = y.search_all(query, threshhold=MAX_SHOW)

        if data:
            if total == 0 or total is None:
                st.write(":pleading_face: みつからなかったです 別な検索キーワードで試してね")
                return
            if total > MAX_SHOW:
                st.text(f"*{MAX_SHOW}件まで取得します")
            df = parse_json_to_df(data)
            st.dataframe(df.drop(columns=columns_to_drop, errors='ignore').reset_index(drop=True))
            st.pydeck_chart(map_pydeck(df))


def main():
    st.title("検索ページ")
    if check_password():
        app()

main()
