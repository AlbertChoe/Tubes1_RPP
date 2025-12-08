"""Streamlit web application for BMW Knowledge Graph Assistant."""

import logging

import streamlit as st

from response_generator import ResponseGenerator
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logging.getLogger("neo4j.notifications").setLevel(logging.WARNING)
PAGE_TITLE = "BMW Knowledge Graph Assistant"
PAGE_ICON = "🚗"
CHAT_HISTORY_LIMIT = 5


def configure_page() -> None:
    st.set_page_config(page_title=PAGE_TITLE, layout="wide")
    st.title(f"{PAGE_ICON} {PAGE_TITLE}")
    st.markdown("Ask questions about BMW models, features, and specifications.")


@st.cache_resource
def get_rag_system() -> ResponseGenerator:
    return ResponseGenerator()


def display_chat_history() -> None:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def handle_user_input(rag: ResponseGenerator) -> None:
    prompt = st.chat_input("Ask about BMW cars (e.g., 'Show me electric SUVs')...")

    if not prompt:
        return

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                recent_history = st.session_state.messages[-CHAT_HISTORY_LIMIT:]
                response = rag.generate_response(prompt, chat_history=recent_history)
                st.markdown(response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
                st.rerun()
            except Exception as e:
                st.error(f"An error occurred: {e}")


def main() -> None:
    configure_page()
    rag = get_rag_system()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    display_chat_history()
    handle_user_input(rag)


if __name__ == "__main__":
    main()
