import streamlit as st
import os
from datetime import datetime
from gemini import generate

ANALYSIS_DIR = os.path.join(os.path.dirname(__file__), "../analysis")

def list_news_files():
    """Return dict mapping display_date_time -> filename"""
    files = []
    for f in os.listdir(ANALYSIS_DIR):
        if f.startswith("analysis_") and f.endswith(".md"):
            try:
                # filename format: analysis_YYYYMMDD_HHMMSS.md
                parts = f.split("_")
                date_part = parts[1]  # YYYYMMDD
                time_part = parts[2].replace(".md", "")  # HHMMSS
                
                dt = datetime.strptime(date_part + time_part, "%Y%m%d%H%M%S")
                # format with AM/PM
                display = dt.strftime("%B %d, %Y %I:%M:%S %p")
                files.append((display, f))
            except Exception:
                continue
    files.sort(key=lambda x: x[0])  # sort by datetime string ascending
    return dict(files)

def load_file_content(filename):
    with open(os.path.join(ANALYSIS_DIR, filename), "r", encoding="utf-8") as f:
        return f.read()

def load_all_files_of_date(date_str):
    """Load and combine all files from the same date (YYYY-MM-DD)"""
    try:
        dt = datetime.strptime(date_str, "%B %d, %Y")
        date_key = dt.strftime("%Y%m%d")
    except ValueError:
        st.error("Invalid date format for combined loading.")
        return None
    
    matching_files = [f for f in os.listdir(ANALYSIS_DIR) if f.startswith(f"analysis_{date_key}_") and f.endswith(".md")]
    matching_files.sort()
    if not matching_files:
        st.warning(f"No files found for date {date_str}")
        return None
    
    combined_content = ""
    for fname in matching_files:
        time_part = fname.split("_")[2].replace(".md", "")
        # convert HHMMSS 24h to 12h with AM/PM
        dt_time = datetime.strptime(time_part, "%H%M%S")
        time_fmt = dt_time.strftime("%I:%M:%S %p")
        with open(os.path.join(ANALYSIS_DIR, fname), "r", encoding="utf-8") as f:
            combined_content += f"\n\n### 🕒 Time: {time_fmt}\n\n" + f.read()
    return combined_content.strip()

def show():
    st.title("🕵️ Hidden Insights from News Stories")

    files_dict = list_news_files()
    if not files_dict:
        st.warning("No news files found in the analysis folder.")
        return

    st.write("Select a news file to analyze (includes date and time):")
    selected_display = st.selectbox("News files", options=list(files_dict.keys()))
    selected_file = files_dict[selected_display]

    combine_all = st.checkbox("Or analyze all files of this date combined", value=False)
    
    if st.button("Reveal Hidden Insights"):
        if combine_all:
            # extract date part only from selected_display
            date_only_str = " ".join(selected_display.split()[:3])  # e.g. "June 09, 2025"
            news_content = load_all_files_of_date(date_only_str)
            if not news_content:
                st.error("No news content found for combined files.")
                return
        else:
            news_content = load_file_content(selected_file)
        
        prompt = f"""
সংবাদ বিশ্লেষণ ({selected_display}):
এখানে উল্লেখিত সংবাদ কনটেন্ট থেকে প্রাপ্ত তথ্যের ভিত্তিতে একটি বিশ্লেষণ দেওয়া হলো:

🔍 প্রধান থিম ও আলোচিত ইস্যুগুলো (Key Themes)
😊/😡/😐 সংবাদের আবেগ বিশ্লেষণ (Sentiment Overview)
📢 জনগণ বনাম সরকার প্রতিক্রিয়া (Public vs Govt Reaction)
🧠 গুরুত্বপূর্ণ কিন্তু কম আলোচিত খবর (Underreported But Critical News)
💬 উল্লেখযোগ্য উক্তি বা বার্তা (Key Narratives or Quotes)
📈 সমাজ বা দেশের উপর প্রভাব (Social Impact)

Please return your response in Bangla with bullet points. Here is the news content:

{news_content}
"""

        with st.spinner("🔍 Extracting hidden insights..."):
            try:
                insights = generate(contents=[prompt])
                st.subheader("📊 Hidden Insights")
                st.markdown(insights)

                # Save insights
                insight_dir = os.path.join(os.path.dirname(__file__), "../insights")
                os.makedirs(insight_dir, exist_ok=True)
                safe_date = selected_display.replace(" ", "_").replace(",", "")
                filename = os.path.join(insight_dir, f"insight_{safe_date}.md")
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(f"# Hidden Insights for {selected_display}\n\n")
                    f.write(insights)

                #st.success(f"✅ Insights saved to {filename}")
                st.success(f"") 


            except Exception as e:
                err_str = str(e).lower()
                if "overloaded" in err_str or "503" in err_str:
                    st.error("currently overloaded. Please try again.")
                    if st.button("🔁 Retry Now"):
                        st.experimental_rerun()
                else:
                    st.error(f"")

if __name__ == "__main__":
    show()
