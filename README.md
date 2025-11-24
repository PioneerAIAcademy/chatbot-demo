# chatbot-demo

Two demo implementations of a streaming chatbot using OpenAI's Responses API.

## Implementations

### 1. Streamlit (`/streamlit`)
- **Architecture**: Single-file Streamlit app with built-in chat UI components
- **File**: `app.py` - Complete chat interface with session state management
- **UI**: Native Streamlit chat widgets (`st.chat_message`, `st.chat_input`)

### 2. FastAPI + Vanilla JS (`/fastapi`)
- **Architecture**: FastAPI backend + HTML/JS frontend with Server-Sent Events
- **Backend**: `main.py` - Streaming `/chat` endpoint using `StreamingResponse`
- **Frontend**: `static/index.html` - Vanilla JavaScript with Fetch API streaming

## Setup

Both apps require an OpenAI API key and use `python-dotenv` to load it:

```bash
# Create .env file in the respective directory
echo "OPENAI_API_KEY=your_key_here" > .env
```

Install dependencies in each directory:
```bash
pip install -r requirements.txt
```

## Running the Apps

### Streamlit App
```bash
cd streamlit
pip install -r requirements.txt
streamlit run app.py
# Opens at http://localhost:8501
```

### FastAPI App
```bash
cd fastapi
pip install -r requirements.txt
python main.py
# Opens at http://localhost:8000

# Optional: customize port and host
python main.py --port 8080 --host localhost
# To expose on network: --host 0.0.0.0
```

## Key Streaming Pattern

Both implementations use the same OpenAI streaming pattern:

```python
stream = client.responses.create(
    model="gpt-4o-mini",
    input=user_message,
    stream=True
)
for event in stream:
    if event.type == "response.output_text.delta":
        # Process delta chunk...
```

The difference is in how they deliver chunks to the user: Streamlit uses placeholders, FastAPI uses HTTP streaming responses.