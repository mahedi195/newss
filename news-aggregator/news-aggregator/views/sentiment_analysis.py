'''
import streamlit as st
import os
import re
from datetime import datetime
import matplotlib.pyplot as plt
import json
from gemini import generate
from gui import get_news_files, get_file_datetime

def parse_sentiment_score(json_str):
    """Extract sentiment scores from JSON string returned by Gemini."""
    try:
        data = json.loads(json_str)
        scores = []
        for day in data.get("days", []):
            score = day.get("sentiment_score")
            if isinstance(score, (int, float)):
                scores.append((day.get("date"), score))
        return scores, data.get("trend_analysis", ""), data.get("topic_trends", [])
    except Exception:
        return [], "", []

def plot_sentiment_trend(scores):
    dates = [datetime.strptime(d, "%Y-%m-%d") for d, _ in scores]
    values = [s for _, s in scores]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, values, marker="o", linestyle="-", color="blue")
    plt.axhline(0, color="gray", linewidth=0.8, linestyle="--")
    plt.title("Sentiment Trend Over Time")
    plt.xlabel("Date")
    plt.ylabel("Sentiment Score (-100 to +100)")
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(plt)

def show():
    st.title("News Sentiment Analysis")

    news_files = get_news_files()
    if not news_files:
        st.warning("No news files found. Please run the crawler first.")
        return

    analysis_option = st.radio(
        "Choose analysis type:",
        ["Single Day Sentiment Analysis", "Sentiment Trend Over Time"]
    )

    if analysis_option == "Single Day Sentiment Analysis":
        file_options = {}
        for file_path in news_files:
            dt = get_file_datetime(file_path)
            if dt:
                display_name = dt.strftime("%B %d, %Y at %I:%M %p")
                file_options[display_name] = file_path

        selected_date = st.selectbox(
            "Select news date:",
            options=list(file_options.keys()),
            index=0
        )
        selected_file = file_options[selected_date]

        if st.button("Analyze Sentiment"):
            with open(selected_file, "r", encoding="utf-8") as f:
                news_content = f.read()

            sentiment_prompt = f"""
            Analyze the sentiment of these news headlines from Bangladesh:

            {news_content}

            Please provide:
            1. Most positive and negative headlines with explanation (বাংলায় লিখুন)
            2. Breakdown of sentiment by news source (বাংলায় লিখুন)
            3. Key topics that are framed positively or negatively (বাংলায় লিখুন)

            Format your response with clear headings and bullet points.
            """

            with st.spinner("Analyzing sentiment..."):
                try:
                    sentiment_analysis = generate(contents=[sentiment_prompt])

                    sentiment_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sentiment")
                    os.makedirs(sentiment_dir, exist_ok=True)

                    date_str = re.search(r"news_(\d{8}_\d{6})\.md", os.path.basename(selected_file)).group(1)
                    filename = os.path.join(sentiment_dir, f"sentiment_{date_str}.md")

                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(f"# News Sentiment Analysis - {selected_date}\n\n")
                        f.write(sentiment_analysis)

                    st.markdown("## Sentiment Analysis Results")
                    st.markdown(sentiment_analysis)
                    st.success(f"Analysis saved to {filename}")

                except Exception as e:
                    st.error(f"Error during sentiment analysis: {str(e)}")

    else:  # Sentiment Trend Over Time
        if len(news_files) < 2:
            st.warning("Need at least two days of news data for trend analysis.")
            return

        num_days = min(len(news_files), 7)
        selected_days = st.slider("Number of days to analyze:", 2, min(len(news_files), 10), num_days)

        if st.button("Analyze Sentiment Trends"):
            with st.spinner(f"Analyzing sentiment trends over {selected_days} days..."):
                trend_data = []

                for file_path in news_files[:selected_days]:
                    dt = get_file_datetime(file_path)
                    date_str = dt.strftime("%Y-%m-%d") if dt else "Unknown"

                    with open(file_path, "r", encoding="utf-8") as f:
                        news_content = f.read()
                        sample_content = "\n".join(news_content.split("\n")[:100])

                        trend_data.append({
                            "date": date_str,
                            "content": sample_content,
                            "file_path": file_path
                        })

                trend_prompt = """
                Analyze the sentiment trends in these news headlines from multiple days in Bangladesh.
                For each day, provide a sentiment score on a scale of -100 (extremely negative) to +100 (extremely positive).

                Also identify key topics and how their sentiment changed over time.

                Respond in this JSON format:
                {
                    "days": [
                        {
                            "date": "YYYY-MM-DD",
                            "sentiment_score": X,
                            "key_topics": ["topic1", "topic2"],
                            "summary": "brief explanation"
                        },
                        ...
                    ],
                    "trend_analysis": "overall analysis of sentiment trends",
                    "topic_trends": [
                        {
                            "topic": "topic name",
                            "trend": "description of how sentiment changed"
                        },
                        ...
                    ]
                }

                Here are the news headlines by day:
                """

                for i, day_data in enumerate(trend_data):
                    trend_prompt += f"\n\nDAY {i+1} ({day_data['date']}):\n{day_data['content']}\n"

                try:
                    trend_analysis_json = generate(contents=[trend_prompt])
                    scores, overall_trend, topic_trends = parse_sentiment_score(trend_analysis_json)

                    if not scores:
                        st.warning("Could not parse sentiment scores from analysis.")
                        st.markdown(trend_analysis_json)
                        return

                    # Save to file
                    trend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "trends")
                    os.makedirs(trend_dir, exist_ok=True)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = os.path.join(trend_dir, f"sentiment_trend_{timestamp}.md")

                    with open(filename, "w", encoding="utf-8") as f:
                        f.write("# News Sentiment Trend Analysis\n\n")
                        f.write(f"Period: Last {selected_days} days\n\n")
                        f.write(trend_analysis_json)

                    st.markdown("## Sentiment Trend Analysis")
                    st.markdown(overall_trend)
                    plot_sentiment_trend(scores)

                    st.markdown("### Topic Sentiment Trends")
                    for topic in topic_trends:
                        st.markdown(f"- **{topic['topic']}**: {topic['trend']}")

                    st.success(f"Trend analysis saved to {filename}")

                except Exception as e:
                    st.error(f"Error during trend analysis: {str(e)}")

                    '''




import streamlit as st
import os
import re
from gemini import generate
from gui import get_news_files, get_file_datetime

def show():
    st.title("News Sentiment Analysis")

    news_files = get_news_files()
    if not news_files:
        st.warning("No news files found. Please run the crawler first.")
        return

    file_options = {}
    for file_path in news_files:
        dt = get_file_datetime(file_path)
        if dt:
            display_name = dt.strftime("%B %d, %Y at %I:%M %p")
            file_options[display_name] = file_path

    selected_date = st.selectbox(
        "Select news date:",
        options=list(file_options.keys()),
        index=0
    )
    selected_file = file_options[selected_date]

    if st.button("Analyze Sentiment"):
        with open(selected_file, "r", encoding="utf-8") as f:
            news_content = f.read()

        sentiment_prompt = f"""
        Analyze the sentiment of these news headlines from Bangladesh:

        {news_content}

        Please provide:
        1. Most positive and negative headlines with explanation (বাংলায় লিখুন)
        2. Breakdown of sentiment by news source (বাংলায় লিখুন)
        3. Key topics that are framed positively or negatively (বাংলায় লিখুন)

        Format your response with clear headings and bullet points.
        """

        with st.spinner("Analyzing sentiment..."):
            try:
                sentiment_analysis = generate(contents=[sentiment_prompt])

                sentiment_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "sentiment")
                os.makedirs(sentiment_dir, exist_ok=True)

                date_str = re.search(r"news_(\d{8}_\d{6})\.md", os.path.basename(selected_file)).group(1)
                filename = os.path.join(sentiment_dir, f"sentiment_{date_str}.md")

                with open(filename, "w", encoding="utf-8") as f:
                    f.write(f"# News Sentiment Analysis - {selected_date}\n\n")
                    f.write(sentiment_analysis)

                st.markdown("## Sentiment Analysis Results")
                st.markdown(sentiment_analysis)
                #st.success(f"Analysis saved to {filename}")
                #st.success(f"Analysis saved to {filename}")

            except Exception as e:
                #st.error(f"Error during sentiment analysis: {str(e)}")
                st.error(f"Please, try aain")
