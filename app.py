import os
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

from utils.reviewer import get_client, is_langsmith_enabled, review_code


load_dotenv()

APP_TITLE = "AI Code Reviewer"
DEFAULT_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")


def init_state() -> None:
    if "history" not in st.session_state:
        st.session_state.history = []


def main() -> None:
    st.set_page_config(page_title=APP_TITLE, layout="wide")
    st.title(APP_TITLE)
    st.caption("Paste source code, choose language, and get an AI-powered review.")

    init_state()

    with st.sidebar:
        st.subheader("Configuration")
        model = st.text_input("Groq model", value=DEFAULT_MODEL)
        st.markdown("---")
        st.markdown("**LangSmith tracing**")
        st.write("Enabled" if is_langsmith_enabled() else "Disabled")

    languages = [
        "python",
        "javascript",
        "typescript",
        "java",
        "go",
        "c",
        "cpp",
        "csharp",
        "rust",
        "php",
        "ruby",
        "kotlin",
        "swift",
        "sql",
        "bash",
        "html",
        "css",
        "json",
        "yaml",
        "other",
    ]

    col1, col2 = st.columns([1, 1])

    with col1:
        language = st.selectbox("Programming language", options=languages, index=0)
        code_input = st.text_area("Paste your source code", height=360, placeholder="def hello():\n    print('Hello world')")
        review_clicked = st.button("Review Code", type="primary")

    with col2:
        st.subheader("Code Preview")
        if code_input.strip():
            st.code(code_input, language=language)
        else:
            st.info("Code preview will appear here after you paste code.")

    if review_clicked:
        if not code_input.strip():
            st.warning("Please paste some code before requesting a review.")
        else:
            try:
                client = get_client()
                with st.spinner("Reviewing code..."):
                    review_markdown = review_code(client, model, language, code_input)

                entry = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "language": language,
                    "model": model,
                    "code": code_input,
                    "review": review_markdown,
                }
                st.session_state.history.insert(0, entry)

                st.success("Review generated.")
            except Exception as exc:
                st.error(f"Failed to generate review: {exc}")

    st.markdown("---")
    st.subheader("Session Review History")

    if not st.session_state.history:
        st.write("No reviews yet in this session.")
    else:
        for i, item in enumerate(st.session_state.history, start=1):
            with st.expander(f"{i}. {item['timestamp']} | {item['language']} | {item['model']}", expanded=(i == 1)):
                st.markdown("### Reviewed Code")
                st.code(item["code"], language=item["language"])
                st.markdown("### AI Review")
                st.markdown(item["review"])


if __name__ == "__main__":
    main()

