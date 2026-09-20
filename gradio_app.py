import gradio as gr
from model import predict_sentiment
def predict(text):    
    result = predict_sentiment(text)    
    return f"{result['label']} ({result['confidence']:.3f})"

demo = gr.Interface( 
    fn=predict,
    inputs="text",
    outputs="text")
demo.launch()
