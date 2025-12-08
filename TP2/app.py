import logging

import streamlit as st

from response_generator import ResponseGenerator

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logging.getLogger("neo4j.notifications").setLevel(logging.WARNING)

st.set_page_config(page_title="BMW Knowledge Graph Assistant", layout="wide")

st.title("🚗 BMW Knowledge Graph Assistant")
st.markdown("""
Ask questions about BMW models, features, and specifications.
""")


@st.cache_resource
def get_rag_system():
    return ResponseGenerator()


rag = get_rag_system()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about BMW cars (e.g., 'Show me electric SUVs')..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                recent_history = st.session_state.messages[-5:]
                response = rag.generate_response(prompt, chat_history=recent_history)
                st.markdown(response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
                st.rerun()
            except Exception as e:
                st.error(f"An error occurred: {e}")
