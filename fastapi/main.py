import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client; relies on OPENAI_API_KEY env var
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

app = FastAPI()

# Serve /static/index.html at /
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def read_root():
    # Tiny convenience redirect to static HTML
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat(req: ChatRequest):
    """
    Streams OpenAI's response text back to the browser as plain text.
    """

    def event_stream():
        # Call the Responses API with streaming on
        # Docs: client.responses.create(..., stream=True) :contentReference[oaicite:1]{index=1}
        response = client.responses.create(
            model="gpt-4o-mini",
            input=req.message,
            stream=True,
        )

        for event in response:
            # Responses streaming emits typed events; we want the text deltas. :contentReference[oaicite:2]{index=2}
            if event.type == "response.output_text.delta":
                # 'delta' is the next chunk of text
                chunk = event.delta
                if chunk:
                    # yield bytes so StreamingResponse can send them
                    yield chunk.encode("utf-8")

    # StreamingResponse will stream chunks as they’re yielded
    return StreamingResponse(event_stream(), media_type="text/plain")


def main():
    """Launch the FastAPI application using uvicorn."""
    import argparse
    import uvicorn

    parser = argparse.ArgumentParser(description="Run FastAPI chatbot server")
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.environ.get("PORT", 8000)),
        help="Port to run the server on (default: 8000)"
    )
    parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="Host to bind to (default: localhost)"
    )
    args = parser.parse_args()

    uvicorn.run("main:app", host=args.host, port=args.port, reload=True)


if __name__ == "__main__":
    main()

