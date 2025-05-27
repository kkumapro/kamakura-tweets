
import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime

st.set_page_config(page_title="鎌倉観光感情マップ", layout="wide")
st.title("📍 鎌倉観光感情マップ（ダミーデータ版）")

# CSVファイルの読み込み（仮の手動CSV）
@st.cache_data
def load_data():
    df = pd.read_csv("kamakura_dummy_tweets.csv")
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["hour"] = df["created_at"].dt.hour
    return df

try:
    df = load_data()
    st.success("✅ ツイートデータを読み込みました")

    # 時間帯の分布チャート
    st.subheader("🕒 ツイートの投稿時間帯（ヒートマップ）")
    hour_chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("hour:O", title="時間帯"),
            y=alt.Y("count():Q", title="ツイート数"),
            tooltip=["hour", "count()"]
        )
        .properties(width=700, height=300)
    )
    st.altair_chart(hour_chart)

    # 感情表現の出現頻度
    st.subheader("😊 感情表現の出現頻度（上位）")
    emotion_keywords = [
        "楽しい", "嬉しい", "最高", "癒される", "感動", "綺麗", "素晴らしい",
        "大好き", "幸せ", "わくわく", "おいしい", "興奮", "満足", "笑顔", "心地よい",
        "感激", "可愛い", "懐かしい", "美味しい", "驚き", "癒し", "感銘", "感無量",
        "涙", "うるうる", "感謝", "愛おしい", "好き", "ほっこり", "感極まる"
    ]

    def count_emotions(text):
        return [word for word in emotion_keywords if word in text]

    all_emotions = df["text"].apply(count_emotions).explode().dropna()
    emotion_count = all_emotions.value_counts().reset_index()
    emotion_count.columns = ["emotion", "count"]

    chart = (
        alt.Chart(emotion_count.head(20))
        .mark_bar()
        .encode(
            x=alt.X("count:Q", title="出現数"),
            y=alt.Y("emotion:N", sort='-x', title="感情キーワード"),
            tooltip=["emotion", "count"]
        )
        .properties(width=700)
    )
    st.altair_chart(chart)

    # 任意のツイートを確認
    st.subheader("🔍 ツイート本文の一覧")
    num = st.slider("表示する件数", 5, 50, 10)
    st.dataframe(df[["created_at", "text"]].sort_values("created_at", ascending=False).head(num))

except Exception as e:
    st.error("❌ データの読み込みに失敗しました。CSVファイルが存在するか確認してください。")
    st.exception(e)
