import streamlit as st
import os
from datetime import datetime
import re
from gemini import generate

def get_file_datetime(filename):
    """Extract datetime from filename in format news_YYYYMMDD_HHMMSS.md"""
    match = re.search(r"news_(\d{8}_\d{6})\.md", os.path.basename(filename))
    if match:
        dt_str = match.group(1)
        return datetime.strptime(dt_str, "%Y%m%d_%H%M%S")
    return None

def show(file_path):
    """Display a specific news file with analysis option"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            news_content = f.read()
        
        dt = get_file_datetime(file_path)
        if dt:
            display_date = dt.strftime("%B %d, %Y at %I:%M %p")
            st.title(f"News Headlines - {display_date}")
        else:
            st.title("News Headlines")
        
        st.markdown(news_content)
        
        # Add analysis button
        if st.button("Analyze with Gemini"):
            with st.spinner("Analyzing news content..."):
                prompt = f"""
                Analyze and summarize the following news headlines from Bangladesh:
                
                {news_content}
                
                Please provide:
                1. A concise summary of the main news stories (বাংলায় লিখুন)
                2. Key themes and trends (বাংলায় লিখুন)
                3. Any significant events worth noting (বাংলায় লিখুন)
                """
                
                try:
                    analysis = generate(contents=[prompt])
                    st.markdown("## News Analysis")
                    st.markdown(analysis)
                    
                    # Save the analysis
                    analysis_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "analysis")
                    os.makedirs(analysis_dir, exist_ok=True)
                    
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = os.path.join(analysis_dir, f"analysis_{timestamp}.md")
                    
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write("# News Analysis\n\n")
                        f.write(analysis)
                    
                    #st.success(f"Analysis saved to {filename}")
                    st.success(f" ")
                    
                    
                except Exception as e:
                    #st.error(f"Error during analysis: {str(e)}")
                    st.error(f" ")
                    
    except Exception as e:
        #st.error(f"Error reading the news file: {str(e)}")
        st.errot("Please, Try again")

