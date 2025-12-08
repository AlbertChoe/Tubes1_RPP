import streamlit as st
import logging
from response_generator import ResponseGenerator

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Suppress Neo4j driver notifications
logging.getLogger("neo4j.notifications").setLevel(logging.WARNING)

st.set_page_config(page_title="BMW Knowledge Graph Assistant", layout="wide")

st.title("🚗 BMW Knowledge Graph Assistant")
st.markdown("""
Ask questions about BMW models, features, and specifications.
""")


# Initialize ResponseGenerator (Cached to avoid reloading)
@st.cache_resource
def get_rag_system():
    return ResponseGenerator()


rag = get_rag_system()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask about BMW cars (e.g., 'Show me electric SUVs')..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = rag.generate_response(prompt)
                st.markdown(response)
                # Add assistant message to history
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
                st.rerun()
            except Exception as e:
                st.error(f"An error occurred: {e}")
