import gradio as gr
from model import predict_sentiment


def predict(text):
    if not text or not text.strip():
        return "Please enter some text."

    result = predict_sentiment(text)
    return f"{result['label']} ({result['confidence']:.3f})"


demo = gr.Interface(
    fn=predict,
    inputs=gr.Textbox(label="Enter text"),
    outputs=gr.Textbox(label="Result"),
    title="AI Sentiment Analysis",
)

if __name__ == "__main__":
    demo.launch()
