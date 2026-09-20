from transformers import pipeline
classifier = pipeline( "sentiment-analysis",  model="distilbert/distilbert-base-uncased-finetuned-sst-2-english")

def predict_sentiment(text:str):    
	result = classifier(text)[0]    
	return {
		"label": result["label"],        
		"confidence": float(result["score"])    
    }

