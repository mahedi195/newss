import streamlit as st
import os
from datetime import datetime
from gemini import generate

def get_analysis_files():
    """Return list of tuples (filename, formatted_date_str) sorted latest first"""
    analysis_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "analysis")
    files = [f for f in os.listdir(analysis_dir) if f.endswith(".md") and f.startswith("analysis_")]
    
    def parse_filename_date(filename):
        # filename like analysis_20250609_215425.md
        try:
            date_str = filename[len("analysis_"):-3]  # remove prefix & .md
            return datetime.strptime(date_str, "%Y%m%d_%H%M%S")
        except Exception:
            return None
    
    file_dates = []
    for f in files:
        dt = parse_filename_date(f)
        if dt:
            file_dates.append((f, dt))
    
    # Sort by datetime descending (latest first)
    file_dates.sort(key=lambda x: x[1], reverse=True)
    
    # Format date for dropdown display with AM/PM: "09 June 2025 09:54:25 PM"
    display_options = [(fname, dt.strftime("%d %B %Y %I:%M:%S %p")) for fname, dt in file_dates]
    return display_options, analysis_dir

def show():
    st.title("🗞️ News Chat Assistant")

    options, analysis_dir = get_analysis_files()
    if not options:
        st.warning("No analysis files found. Please run the crawler/analysis first.")
        return
    
    # Map displayed date string to filename for selection
    display_dates = [display for _, display in options]
    filename_map = {display: fname for fname, display in options}
    
    selected_display_date = st.selectbox(
        "📅 Select news date and time",
        display_dates
    )
    
    selected_filename = filename_map[selected_display_date]
    selected_path = os.path.join(analysis_dir, selected_filename)
    
    # Load content from selected file
    try:
        with open(selected_path, "r", encoding="utf-8") as f:
            news_content = f.read()
    except Exception as e:
        st.error(f"Failed to load selected file: {e}")
        return

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask me about the selected news file"):
        # Add a line before user question showing the selected date and time
        prompt_with_date = f"Date and time: {selected_display_date}\n\nUser question: {prompt}"

        st.session_state.messages.append({"role": "user", "content": prompt_with_date})

        with st.chat_message("user"):
            st.markdown(prompt_with_date)

        if not news_content.strip():
            error_message = "The selected file is empty."
            st.chat_message("assistant").markdown(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})
            return

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                full_prompt = f"""
                You are a helpful news assistant for Bangladesh news.
                Use the following news content as context to answer the user's question.
                If the answer cannot be found in the news content, politely say so.

                NEWS CONTENT:
                {news_content}

                USER QUESTION:
                Date and time: {selected_display_date}

                {prompt}
                """
                try:
                    response = generate(contents=[full_prompt])
                    st.markdown(response)

                    st.session_state.messages.append({"role": "assistant", "content": response})

                    # Save chat to chats/
                    chat_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chats")
                    os.makedirs(chat_dir, exist_ok=True)

                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    chat_file = os.path.join(chat_dir, f"chat_{timestamp}.md")

                    with open(chat_file, "w", encoding="utf-8") as f:
                        f.write("# News Chat Session\n\n")
                        for msg in st.session_state.messages:
                            f.write(f"## {msg['role'].title()}\n")
                            f.write(f"{msg['content']}\n\n")

                except Exception as e:
                    #st.error(f"Error generating response: {str(e)}")
                    st.error(f"please , try later")
                    st.session_state.messages.append({"role": "assistant", "content": f"Error: {str(e)}"})

    if st.session_state.messages:
        if st.button("🧹 Clear Chat History"):
            st.session_state.messages = []
            st.experimental_rerun()
