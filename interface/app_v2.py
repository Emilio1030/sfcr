import streamlit as st
from praisonaiagents import Agent

def init_agent():
    config = {
        "vector_store": {
            "provider": "chroma",
            "config": {
                "collection_name": "praison",
                "path": ".praison"
            }
        },
        "llm": {
            "provider": "ollama",
            "config": {
                "model": "deepseek-r1:latest",
                "temperature": 0,
                "max_tokens": 8000,
                "ollama_base_url": "http://localhost:11434",
            },
        },
        "embedder": {
            "provider": "ollama",
            "config": {
                "model": "nomic-embed-text:latest",
                "ollama_base_url": "http://localhost:11434",
                "embedding_dims": 1536
            },
        },
    }

    return Agent(
        name="Knowledge Agent",
        instructions="You answer questions based on the provided knowledge.",
        knowledge=["/Users/emilioaguiar/code/Emilio1030/sfcr/output/1097_SFCR_2023/auto/1097_SFCR_2023.md"],
        knowledge_config=config,
        user_id="user1",
        llm="deepseek-r1"
    )

st.title("Knowledge Agent Chat")

# Initialize the agent and messages in session state
if "agent" not in st.session_state:
    st.session_state.agent = init_agent()
    st.session_state.messages = []

# Display previous messages
if "messages" in st.session_state:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Get user input
prompt = st.chat_input("Ask a question...")

if prompt:
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display the assistant's response
    with st.chat_message("assistant"):
        response = st.session_state.agent.start(prompt)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
