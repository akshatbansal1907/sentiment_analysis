from fastapi import FastAPI
from pydantic import BaseModel
import gradio as gr

from model import predict_sentiment

# Create FastAPI application
app = FastAPI(
    title="Sentiment Analysis API",
    description="Sentiment analysis using DistilBERT",
    version="1.0"
)

# Request model
class TextInput(BaseModel):
    text: str

# Home endpoint
@app.get("/")
def home():
    return {
        "message": "Sentiment Analysis API is working!"
    }

# Sentiment API endpoint
@app.post("/sentiment")
def sentiment_analysis(data: TextInput):

    result = predict_sentiment(data.text)

    return {
        "text": data.text,
        "sentiment": result["label"],
        "confidence": result["confidence"]
    }

# Function used by Gradio
def predict_for_gradio(text):

    if not text or not text.strip():
        return "Please enter some text."

    result = predict_sentiment(text)

    return (
        f"Sentiment: {result['label']}\n"
        f"Confidence: {result['confidence']:.3f}"
    )

# Gradio interface
demo = gr.Interface(
    fn=predict_for_gradio,
    inputs=gr.Textbox(
        label="Enter text",
        placeholder="Type something like: I love this product!"
    ),
    outputs=gr.Textbox(
        label="Result"
    ),
    title="AI Sentiment Analysis",
    description="Enter text and the AI will predict whether it is positive or negative."
)

# Mount Gradio inside FastAPI
app = gr.mount_gradio_app(
    app,
    demo,
    path="/gradio"
)