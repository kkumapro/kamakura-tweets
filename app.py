
import streamlit as st
import pandas as pd

st.set_page_config(page_title="鎌倉観光感情マップ", layout="centered")

st.title("🌸 鎌倉観光ツイート 感情マップ")

# 感情判定ルールベース関数
def simple_sentiment(text):
    positive_words = ["最高", "楽しい", "素晴らしい", "感動", "美しい", "満足", "嬉しい", "癒し", "良かった"]
    negative_words = ["疲れた", "最悪", "混んでる", "うるさい", "微妙", "残念", "つまらない", "イライラ"]

    if any(word in text for word in positive_words):
        return "positive"
    elif any(word in text for word in negative_words):
        return "negative"
    else:
        return "neutral"

# ツイート表示関数（感情別に装飾）
def display_tweet(text, sentiment):
    if sentiment == "positive":
        st.markdown(f'<span style="color:red;">😊 {text}</span>', unsafe_allow_html=True)
    elif sentiment == "negative":
        st.markdown(f'<span style="color:blue;">😞 {text}</span>', unsafe_allow_html=True)
    else:
        st.markdown(f'<span style="color:gray;">😐 {text}</span>', unsafe_allow_html=True)

# CSVファイル読み込み
try:
    df = pd.read_csv("kamakura_tweets.csv")
    if "text" not in df.columns:
        st.error("CSVファイルに'text'列がありません。")
    else:
        df["sentiment"] = df["text"].apply(simple_sentiment)

        st.subheader("📋 感情付きツイート一覧")
        for _, row in df.iterrows():
            display_tweet(row["text"], row["sentiment"])
except FileNotFoundError:
    st.warning("❗ kamakura_tweets.csv が見つかりません。ファイルをアップロードしてください。")
    uploaded_file = st.file_uploader("CSVファイルをアップロード", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        if "text" in df.columns:
            df["sentiment"] = df["text"].apply(simple_sentiment)
            st.success("ファイルを読み込みました！")

            st.subheader("📋 感情付きツイート一覧")
            for _, row in df.iterrows():
                display_tweet(row["text"], row["sentiment"])
        else:
            st.error("アップロードされたCSVに'text'列が含まれていません。")
