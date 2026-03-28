from flask import Flask, request, jsonify, render_template
from transformers import pipeline
from pymongo import MongoClient
import datetime

app = Flask(__name__)

# Load sentiment model
sentiment_pipeline = pipeline("sentiment-analysis")

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["sentiment_db"]
collection = db["results"]

# Home page
@app.route('/')
def home():
    return render_template('index.html')

# Analyze sentiment
@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form['text']
    
    result = sentiment_pipeline(text)[0]
    
    sentiment = result['label']
    score = result['score']
    
    # Store in MongoDB
    data = {
        "text": text,
        "sentiment": sentiment,
        "score": score,
        "timestamp": datetime.datetime.now()
    }
    collection.insert_one(data)
    
    return jsonify({
        "text": text,
        "sentiment": sentiment,
        "score": round(score, 3)
    })

# Get all results
@app.route('/results', methods=['GET'])
def results():
    data = list(collection.find({}, {"_id": 0}))
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)