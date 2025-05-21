
import streamlit as st
import pandas as pd
import altair as alt

st.title("鎌倉リアルタイムツイート可視化")

# 仮のデータ（後でリアルタイム収集に置き換える）
df = pd.read_csv("kamakura_tweets.csv")

st.subheader("ツイート一覧")
st.dataframe(df)

st.subheader("投稿時間の分布")
chart = alt.Chart(df).mark_bar().encode(
    x='hour',
    y='count()'
)
st.altair_chart(chart, use_container_width=True)
