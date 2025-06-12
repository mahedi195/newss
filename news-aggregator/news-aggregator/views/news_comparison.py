

import streamlit as st
import os
from datetime import datetime
from gemini import generate

def get_analysis_files():
    analysis_dir = os.path.join(os.path.dirname(__file__), "../analysis")
    if not os.path.exists(analysis_dir):
        return []

    # List all analysis files with full path
    files = [
        (f, os.path.join(analysis_dir, f))
        for f in os.listdir(analysis_dir)
        if f.startswith("analysis_") and f.endswith(".md")
    ]

    # Sort by datetime in filename, newest first
    files.sort(key=lambda x: extract_datetime_from_filename(x[0]), reverse=True)
    return files

def extract_datetime_from_filename(filename):
    try:
        # Filename: analysis_YYYYMMDD_HHMMSS.md
        parts = filename.split("_")
        date_str = parts[1] + "_" + parts[2].replace(".md", "")
        return datetime.strptime(date_str, "%Y%m%d_%H%M%S")
    except Exception:
        return datetime.min  # fallback for sorting

def get_label_for_dropdown(filename):
    dt = extract_datetime_from_filename(filename)
    return dt.strftime("%d %B %Y - %I:%M:%S %p")

def load_analysis(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def show():
    st.title("📰 Compare News Between Two Dates")

    analysis_files = get_analysis_files()
    if not analysis_files:
        st.warning("No analysis files found in the analysis/ folder.")
        return

    # Create dropdown options: {label: filepath}
    options = {get_label_for_dropdown(f): path for f, path in analysis_files}
    labels = list(options.keys())

    col1, col2 = st.columns(2)
    with col1:
        choice1 = st.selectbox("🗓️ Select First Analysis", labels)
    with col2:
        choice2 = st.selectbox("🗓️ Select Second Analysis", labels)

    if st.button("📊 Compare"):
        if choice1 == choice2:
            st.warning("Please choose two different analysis files.")
            return

        content1 = load_analysis(options[choice1])
        content2 = load_analysis(options[choice2])

        with st.spinner("Comparing the two analyses..."):
            prompt = f"""
Compare the news coverage between these two times:

### News on {choice1}:
{content1}

### News on {choice2}:
{content2}

Identify:
1. What happened on {choice1} but not on {choice2} (বাংলায় লিখুন)
2. What happened on {choice2} but not on {choice1} (বাংলায় লিখুন)
3. Any similarities or follow-ups (বাংলায় লিখুন)
4. Clear bullet-pointed insights in বাংলা

Respond in Markdown format.
"""
            try:
                result = generate(contents=[prompt])
                st.subheader("📄 Comparison Result")
                st.markdown(result)

                # Save output
                comp_dir = os.path.join(os.path.dirname(__file__), "../comparisons")
                os.makedirs(comp_dir, exist_ok=True)
                save_name = f"comparison_{choice1.replace(':','').replace(' ','_')}_vs_{choice2.replace(':','').replace(' ','_')}.md"
                with open(os.path.join(comp_dir, save_name), "w", encoding="utf-8") as f:
                    f.write(f"# News Comparison: {choice1} vs {choice2}\n\n{result}")

                #st.success(f"Comparison saved to comparisons/{save_name}")
                st.success(f"")
            except Exception as e:
                #st.error(f"Error comparing files: {str(e)}")
                st.error(f"")
