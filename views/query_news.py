
import os
import glob
from dateutil import parser
import streamlit as st

# Folder containing analysis markdown files
ANALYSIS_DIR = os.path.join("analysis")

def get_date_key(user_input):
    try:
        dt = parser.parse(user_input)
        return dt.strftime("%Y%m%d")
    except Exception:
        return None

def find_analysis_files(date_key):
    pattern = os.path.join(ANALYSIS_DIR, f"analysis_{date_key}_*.md")
    matches = glob.glob(pattern)
    return matches

def load_file_content(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"❌ Error reading file: {str(e)}"

def get_available_dates():
    # Find all analysis files, extract date keys from filenames, return unique sorted dates
    pattern = os.path.join(ANALYSIS_DIR, "analysis_*.md")
    files = glob.glob(pattern)
    dates = set()
    for fpath in files:
        filename = os.path.basename(fpath)
        # Filename format: analysis_YYYYMMDD_xxx.md
        parts = filename.split('_')
        if len(parts) > 1 and len(parts[1]) == 8 and parts[1].isdigit():
            dates.add(parts[1])
    return sorted(list(dates), reverse=True)  # most recent first

def format_date_key(date_key):
    # Convert YYYYMMDD string to readable date, e.g. 20250609 -> June 9, 2025
    try:
        dt = parser.parse(date_key)
        return dt.strftime("%B %d, %Y")
    except Exception:
        return date_key

def show():
    st.header("🔍 Search News by Date")

    available_dates = get_available_dates()
    if not available_dates:
        st.warning("No analysis files found in the analysis folder.")
        return

    # Create a dropdown with formatted date options
    options = {format_date_key(d): d for d in available_dates}
    selected_date_str = st.selectbox("Select a date:", options.keys())
    selected_date_key = options[selected_date_str]

    matches = find_analysis_files(selected_date_key)

    if matches:
        st.success(f"📰 Found {len(matches)} analyzed news file(s) for: {selected_date_str}")
        for file_path in sorted(matches):
            filename = os.path.basename(file_path)
            content = load_file_content(file_path)
            st.markdown(f"### 📄 {filename}")
            st.markdown(content)

            with open(file_path, "rb") as f:
                st.download_button(
                    label="⬇️ Download this file",
                    data=f,
                    file_name=filename,
                    mime="text/markdown"
                )
            st.markdown("---")  # separator between files
    else:
        st.error(f"❌ No analyzed news found for {selected_date_str}.")




