import streamlit as st
import pandas as pd
import numpy as np

import pandas_datareader.data as web

from datetime import datetime, timedelta
import plotly.graph_objects as go

# データ辞書の定義
data_dict = {9432: 'ＮＴＴ日本', 9433: 'ＫＤＤＩ', 9434: 'ソフトバンク',
             9613: 'ＮＴＴデータ', 9984: 'ソフトバンクグループ'}
data_list = [k for k in data_dict.keys()]

# サイドバーで銘柄コードを選択
ticker = st.sidebar.selectbox('銘柄コードを選択してください', data_list)
st.text('コード : {0} , 銘柄: {1}'.format(ticker, data_dict[ticker]))

# 銘柄コードとデータソースの設定
stock_code = '{0}.JP'.format(ticker)
data_source = 'stooq'

# 日付の設定
today = datetime.today()
end_date = today.strftime('%Y-%m-%d')
start_date = (today - timedelta(days=30)).strftime('%Y-%m-%d')

# データの取得
try:
    df = web.DataReader(stock_code, data_source=data_source, start=start_date, end=end_date)
    df = df.sort_index()
except Exception as e:
    st.error(f"データの取得中にエラーが発生しました: {e}")

# グラフの描画
x = np.arange(df.shape[0])
interval = 1
vals = np.arange(df.shape[0], step=interval)
labels = list(df.index[::interval].strftime('%Y-%m-%d'))

fig = go.Figure(
    data=[go.Candlestick(
        x=x,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close']),
    ],
    layout=go.Layout(
        xaxis=dict(
            tickvals=vals,
            ticktext=labels,
            tickangle=-45
        ),
    )
)

config = {'modeBarButtonsToAdd': ['drawline']}
st.plotly_chart(fig, use_container_width=True, config=config)