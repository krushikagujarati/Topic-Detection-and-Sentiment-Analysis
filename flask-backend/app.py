from flask import Flask, request, jsonify
from transformers import pipeline
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

# Load Hugging Face models
sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
topic_classifier = pipeline("zero-shot-classification")

# Predefined topic categories
TOPIC_CATEGORIES = ["Politics", "Sports", "Technology", "Health", "Business", "Entertainment"]

# Web scraping function using requests and BeautifulSoup
def scrape_headlines(url, start_index=0, batch_size=2):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return {"error": f"Failed to fetch data. HTTP Status Code: {response.status_code}"}
    soup = BeautifulSoup(response.text, 'html.parser')
    elements = soup.find_all('h2')  # Update as needed
    headlines = [element.text.strip() for element in elements]
    return headlines[start_index:start_index + batch_size]

@app.route('/scrape-headlines', methods=['POST'])
def scrape_headlines_endpoint():
    data = request.json
    url = data.get("url")
    start_index = data.get("start_index", 0)
    batch_size = data.get("batch_size", 2)

    if not url:
        return jsonify({"error": "URL not provided"}), 400

    headlines = scrape_headlines(url, start_index, batch_size)
    if not headlines:
        return jsonify({"error": "No more headlines found"}), 400

    return jsonify({"headlines": headlines})

@app.route('/process-headlines', methods=['POST'])
def process_headlines():
    data = request.json
    headlines = data.get("headlines", [])

    if not headlines:
        return jsonify({"error": "No headlines provided"}), 400

    results = []
    for headline in headlines:
        # Sentiment Analysis
        sentiment_result = sentiment_analyzer(headline)[0]

        # Topic Detection
        topic_result = topic_classifier(headline, candidate_labels=TOPIC_CATEGORIES)
        detected_topic = topic_result['labels'][0]  # Most probable topic

        results.append({
            "headline": headline,
            "sentiment": sentiment_result['label'],
            "confidence": sentiment_result['score'],
            "topic": detected_topic
        })

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
