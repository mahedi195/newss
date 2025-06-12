import streamlit as st
import os
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
from gemini import generate
from gui import get_news_files, get_file_datetime

def show():
    """Display trending topics and analysis over time"""
    st.title("News Trend Analysis")
    
    news_files = get_news_files()
    
    if len(news_files) < 2:
        st.warning("Need at least two days of news data for trend analysis. Please run the crawler for multiple days.")
        return
    
    # Determine the time span available
    dates = []
    for file_path in news_files:
        dt = get_file_datetime(file_path)
        if dt:
            dates.append(dt.strftime("%Y-%m-%d"))
    
    unique_dates = sorted(set(dates), reverse=True)
    
    st.subheader("Available Data Timespan")
    st.write(f"From {unique_dates[-1]} to {unique_dates[0]}")
    
    # Time period selection
    time_period = st.selectbox(
        "Select time period to analyze:",
        ["All available data", "Last 3 days", "Last week", "Custom"]
    )
    
    if time_period == "Custom":
        selected_dates = st.multiselect(
            "Select dates to include in analysis:",
            options=unique_dates,
            default=unique_dates[:min(3, len(unique_dates))]
        )
        
        if not selected_dates:
            st.warning("Please select at least one date.")
            return
            
        files_to_analyze = [f for f in news_files if any(d in os.path.basename(f) for d in selected_dates)]
    else:
        if time_period == "Last 3 days":
            num_days = min(3, len(news_files))
        elif time_period == "Last week":
            num_days = min(7, len(news_files))
        else:  # All available data
            num_days = len(news_files)
            
        files_to_analyze = news_files[:num_days]
    
    # Analysis type
    analysis_type = st.radio(
        "Choose analysis type:",
        ["Topic Trends", "Key People & Organizations", "Issue Evolution"]
    )
    
    if st.button("Analyze Trends"):
        with st.spinner("Analyzing news trends..."):
            try:
                # Collect content from selected files
                contents = []
                file_dates = []
                
                for file_path in sorted(files_to_analyze, key=lambda x: os.path.basename(x)):
                    dt = get_file_datetime(file_path)
                    date_str = dt.strftime("%Y-%m-%d") if dt else "Unknown"
                    file_dates.append(date_str)
                    
                    with open(file_path, "r", encoding="utf-8") as f:
                        # Only get first 100 lines to avoid token limits
                        content = "\n".join(f.read().split("\n")[:100])
                        contents.append((date_str, content))
                
                # Generate prompt based on analysis type
                if analysis_type == "Topic Trends":
                    prompt = """
                    Analyze these news articles to identify trending topics over time. (বাংলায় লিখুন)
                    Identify which topics are rising, falling, or remaining consistent in coverage. (বাংলায় লিখুন)
                    
                    For each date, identify the top 5 topics and provide a brief explanation of how coverage has changed. (বাংলায় লিখুন)
                    
                    Also identify any emerging topics that weren't present in earlier coverage.(বাংলায় লিখুন)
                    
                    Format your response with clear headings and sections.(বাংলায় লিখুন)
                    """
                elif analysis_type == "Key People & Organizations":
                    prompt = """
                    Analyze these news articles to track mentions of key people, organizations, and institutions over time.(বাংলায় লিখুন)
                    
                    Identify which individuals or organizations are receiving increasing or decreasing coverage.(বাংলায় লিখুন)
                    Note any shifts in how they are portrayed in the news.(বাংলায় লিখুন)
                    
                    Format your response with clear headings and sections. (বাংলায় লিখুন)
                    """
                else:  # Issue Evolution
                    prompt = """
                    Analyze how the framing and discussion of major issues has evolved over the time period in these news articles.
                    
                    For major issues, track:
                    1. How the issue is described (বাংলায় লিখুন)
                    2. What solutions are proposed (বাংলায় লিখুন)
                    3. Which stakeholders are mentioned (বাংলায় লিখুন)
                    4. Any shift in perceived importance (বাংলায় লিখুন)
                    
                    Format your response with clear headings and sections.
                    """
                
                # Add all the content to the prompt
                prompt += "\n\nNews articles by date:\n"
                for date_str, content in contents:
                    prompt += f"\n\nDATE: {date_str}\n{content}\n"
                
                try:
                    trend_analysis = generate(contents=[prompt])
                    
                    # Save the analysis
                    analysis_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "trends")
                    os.makedirs(analysis_dir, exist_ok=True)
                    
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = os.path.join(analysis_dir, f"{analysis_type.lower().replace(' ', '_')}_{timestamp}.md")
                    
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(f"# {analysis_type} Analysis\n\n")
                        f.write(f"Period: {file_dates[-1]} to {file_dates[0]}\n\n")
                        f.write(trend_analysis)
                    
                    st.markdown(f"## {analysis_type} Analysis Results")
                    st.markdown(trend_analysis)
                    #st.success(f"Analysis saved to {filename}")
                    st.success(f"")

                    
                except Exception as e:
                    #st.error(f"Error generating analysis: {str(e)}")
                    st.error(f"Please, try again")

                    
            except Exception as e:
                #st.error(f"Error processing news files: {str(e)}")
                st.error(f"Please, try again")

