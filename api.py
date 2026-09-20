from fastapi import FastAPI
from pydantic import BaseModel
import gradio as gr

from model import predict_sentiment

app = FastAPI(
    title="Sentiment Analysis API",
    description="Lightweight sentiment analysis using a DistilBERT-based model",
    version="2.0",
)


class TextInput(BaseModel):
    text: str


@app.get("/")
def home():
    return {"message": "Sentiment Analysis API is working!"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/sentiment")
def sentiment_analysis(data: TextInput):
    result = predict_sentiment(data.text)

    return {
        "text": data.text,
        "sentiment": result["label"],
        "confidence": result["confidence"],
    }


def predict_for_gradio(text):
    if not text or not text.strip():
        return "Please enter some text."

    result = predict_sentiment(text)

    return (
        f"Sentiment: {result['label']}\n"
        f"Confidence: {result['confidence']:.3f}"
    )


demo = gr.Interface(
    fn=predict_for_gradio,
    inputs=gr.Textbox(
        label="Enter text",
        placeholder="Type something like: I love this product!",
        lines=5,
    ),
    outputs=gr.Textbox(label="Result"),
    title="AI Sentiment Analysis",
    description="Enter text and the AI will predict whether it is positive or negative.",
)

app = gr.mount_gradio_app(app, demo, path="/gradio")
