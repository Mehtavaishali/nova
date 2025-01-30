from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Azure Text Analytics API configuration
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")  # Read from .env file
AZURE_KEY = os.getenv("AZURE_KEY")  # Read from .env file

# Route to handle text analysis requests
@app.route('/analyze', methods=['POST'])
def analyze_text():
    # Get the text from the frontend
    data = request.json
    text = data.get('text')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    # Prepare the request to Azure Text Analytics
    url = f"{AZURE_ENDPOINT}/text/analytics/v3.1/sentiment"
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': AZURE_KEY
    }
    body = {
        "documents": [
            {
                "id": "1",
                "language": "en",
                "text": text
            }
        ]
    }

    try:
        # Send the request to Azure
        response = requests.post(url, headers=headers, json=body)
        response.raise_for_status()  # Raise an error for bad status codes
        result = response.json()

        # Extract and return the analysis results
        if result.get('documents'):
            sentiment = result['documents'][0]['sentiment']
            confidence_scores = result['documents'][0]['confidenceScores']
            return jsonify({
                'sentiment': sentiment,
                'confidence_scores': confidence_scores
            })
        else:
            return jsonify({'error': 'No analysis results found'}), 500

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Failed to analyze text: {str(e)}'}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)