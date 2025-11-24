# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the Streamlit implementation of a streaming chatbot demo. The parent directory (`/home/dallan/pioneeracademy/chatbot-demo/`) contains two separate implementations:
- **streamlit/** - This directory: Streamlit-based chatbot UI
- **fastapi/** - FastAPI backend with vanilla HTML/JS frontend

Both implementations demonstrate OpenAI's Responses API with streaming capabilities but use different frameworks.

## Architecture

### Streamlit Implementation (this directory)

**Single-file application**: `app.py` contains the entire Streamlit app
- Uses Streamlit's built-in `st.chat_message()` and `st.chat_input()` for UI
- Maintains conversation history in `st.session_state.messages`
- Calls `client.responses.create()` with `stream=True` to get streaming responses
- Iterates over events, looking for `event.type == "response.output_text.delta"`
- Updates UI in real-time using `st.empty()` placeholder and markdown

**Key API pattern**:
```python
stream = client.responses.create(
    model="gpt-4o-mini",
    input=user_input,
    stream=True,
)
for event in stream:
    if event.type == "response.output_text.delta":
        delta = event.delta or ""
        # Process delta...
```

### FastAPI Implementation (sibling directory)

**Structure**:
- `main.py` - FastAPI backend with `/chat` endpoint
- `static/index.html` - Vanilla JS frontend with Fetch API streaming

**Key difference**: FastAPI uses `StreamingResponse` and yields chunks as bytes, while Streamlit uses placeholders and markdown rendering.

## Development Commands

### Setup
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Linux/Mac
# .venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
# Create .env file with: OPENAI_API_KEY=your_key_here
```

### Running the Application
```bash
# Run Streamlit app (from streamlit/ directory)
streamlit run app.py

# Default: http://localhost:8501
```

### For FastAPI version (from fastapi/ directory)
```bash
python main.py
# Default: http://localhost:8000
# Optional arguments: --port 8000 --host localhost

# To expose on network: --host 0.0.0.0
# Alternative: use uvicorn directly
# uvicorn main:app --reload
```

## Environment Configuration

**Required**: `OPENAI_API_KEY` must be set in `.env` file or environment
- Both implementations use `os.environ.get("OPENAI_API_KEY")`
- The `.env` file is gitignored for security

## Dependencies

**Streamlit version**:
- `streamlit` - Web framework with built-in chat UI components
- `openai` - OpenAI Python SDK for Responses API
- `python-dotenv` - Loads environment variables from .env file

**FastAPI version**:
- `fastapi` - Web framework
- `uvicorn[standard]` - ASGI server
- `openai` - OpenAI Python SDK
- `python-dotenv` - Loads environment variables from .env file

## Modifying the Chatbot

To change the OpenAI model: Edit the `model` parameter in `client.responses.create()` call
- Current: `"gpt-4o-mini"` (both implementations)
- Alternative: `"gpt-4o"`

To modify UI appearance: Streamlit uses built-in chat components; customization is limited to Streamlit's theming options
