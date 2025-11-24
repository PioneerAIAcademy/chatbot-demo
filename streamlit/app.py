import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client (uses OPENAI_API_KEY env var)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

st.set_page_config(page_title="Streaming Chatbot (Streamlit)", page_icon="💬")

st.title("💬 Streaming Chatbot (Streamlit + OpenAI)")

st.write(
    "Type a message below. The response from OpenAI will stream in real time.\n"
    "This app uses the Responses API with streaming turned on."
)

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []  # each item: {"role": "user"/"assistant", "content": "..."}

# Display existing chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input (Streamlit's chat-style input)
user_input = st.chat_input("Say something...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Placeholder for streaming assistant response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_text = ""

        # Call Responses API with streaming
        stream = client.responses.create(
            model="gpt-4o-mini",
            input=user_input,
            stream=True,
        )

        # Iterate over Events and update text as we get deltas
        for event in stream:
            if event.type == "response.output_text.delta":
                delta = event.delta or ""
                full_text += delta
                response_placeholder.markdown(full_text)

        # Save full assistant message to history
        st.session_state.messages.append(
            {"role": "assistant", "content": full_text}
        )

