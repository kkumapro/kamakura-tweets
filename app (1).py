import streamlit as st
import requests
import pandas as pd

BEARER_TOKEN = st.secrets["BEARER_TOKEN"]

headers = {
    "Authorization": f"Bearer {BEARER_TOKEN}"
}

query = "鎌倉 -is:retweet lang:ja"
url = f"https://api.twitter.com/2/tweets/search/recent?query={query}&max_results=20&tweet.fields=created_at"

response = requests.get(url, headers=headers)

if response.status_code == 200:
    tweets = response.json()
    if "data" in tweets:
        data = [{
            "text": t["text"],
            "created_at": t["created_at"]
        } for t in tweets["data"]]

        df = pd.DataFrame(data)
        df["created_at"] = pd.to_datetime(df["created_at"])
        df["hour"] = df["created_at"].dt.hour

        st.write("✅ ツイート取得成功！")
        st.dataframe(df)
    else:
        st.warning("⚠️ ツイートデータが見つかりませんでした。")
else:
    st.error(f"❌ ツイート取得に失敗しました（Status Code: {response.status_code}）")
