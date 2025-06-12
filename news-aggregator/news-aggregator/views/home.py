
import streamlit as st
from datetime import datetime
import os
from gemini import generate

def get_latest_news_content():
    """Get content of the latest news file"""
    from gui import get_news_files
    
    news_files = get_news_files()
    if not news_files:
        return None
    
    try:
        with open(news_files[0], "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return None

def show():
    """Display the home page with the latest news and analysis option"""
    st.title("Latest News ")
    
    news_content = get_latest_news_content()
    
    if news_content:
        # st.markdown("## Latest Headlines")
        # st.markdown(news_content)
        
        # Add analysis button
        if st.button("Analyze News"):
            with st.spinner("Analyzing news content..."):
                prompt = f"""
                Analyze and summarize the following news headlines from Bangladesh:
                
                {news_content}
                
                Please provide:
                1. A concise summary of the main news stories in bangla with newspaper name, 
                  published time , sentiment (posiitive/negative) , political level-pro-govt./anti-govt/neutral and 2-3 sentence description (বাংলায় লিখুন) 
                2. A concise summary of the main news stories in english from english newspaper with newspaper name, 
                  published time , sentiment (posiitive/negative) , political level-pro-govt./anti-govt/neutral  and 2-3 sentence description (ইংরেজি লিখুন)
                3. A concise summary of the main news stories in facebook pages  with facebook page name, 
                  published time , sentiment (posiitive/negative) , political level-pro-govt./anti-govt/neutral and 2-3 sentence description (বাংলায় লিখুন)
                4. Key themes and trends (বাংলায় লিখুন)
                5. Any significant events worth noting (বাংলায় লিখুন)
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
                    st.success(f"")
                    
                except Exception as e:
                    #st.error(f"Error during analysis: {str(e)}")
                    st.error(f"")
    else:
        st.warning("No news content available. Please run the crawler first.")