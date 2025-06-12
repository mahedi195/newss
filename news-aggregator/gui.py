import streamlit as st
import os
import glob
import re
from datetime import datetime

NEWS_DIR = os.path.join(os.path.dirname(__file__), "news")

def get_news_files():
    if not os.path.exists(NEWS_DIR):
        return []
    return sorted(
        glob.glob(os.path.join(NEWS_DIR, "news_*.md")),
        key=os.path.getmtime,
        reverse=True
    )

def get_file_datetime(filename):
    match = re.search(r"news_(\d{8}_\d{6})\.md", os.path.basename(filename))
    return datetime.strptime(match.group(1), "%Y%m%d_%H%M%S") if match else None

def load_view(page):
    views = {
        "News": "views.home",
        "Chat with News": "views.chat",
        "News Comparison": "views.news_comparison",
        "Sentiment Analysis": "views.sentiment_analysis",
        "Search News by Date": "views.query_news",
        "Hidden Insights from News": "views.hidden_insights"
    }
    if page in views:
        module = __import__(views[page], fromlist=["show"])
        module.show()

def main():
    st.set_page_config(page_title="Dhaka News Headlines", page_icon="📰", layout="wide")

    with st.sidebar:
        st.title("Dhaka News Explorer")
        st.header("Navigation")
        page = st.radio("Go to:", [
            "News",
            "Chat with News",
            "News Comparison",
            "Sentiment Analysis",
            "Search News by Date",
            "Hidden Insights from News"
        ])

    load_view(page)

if __name__ == "__main__":
    main()



