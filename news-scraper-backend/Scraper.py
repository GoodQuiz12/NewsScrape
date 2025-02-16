import os
import logging
from dotenv import load_dotenv # type: ignore
from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import requests
import json  # For JSON handling

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure CORS - Specific origin for development
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}}) # Adjust origin if your frontend port is different in development

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- NewsAPI Configuration ---
NEWSAPI_KEY = "NEWSAPI_KEY" # Get API key from environment variable
NEWSAPI_ENDPOINT = "https://newsapi.org/v2/everything"

# --- Social Media Configuration (Placeholder) ---
SOCIAL_MEDIA_SITES = {}  # No social media in this example for simplicity


def fetch_news_from_api(topic, sources=None):
    """Fetches news from NewsAPI based on the topic and optional sources."""
    if not NEWSAPI_KEY:
        logger.error("NEWSAPI_KEY is not set. Please set it in your .env file.")
        return []  # Return empty list if API key is missing

    try:
        params = {
            "q": topic,  # User-provided topic as query
            "apiKey": NEWSAPI_KEY,
            "language": "en",  # You can change language if needed
            "sortBy": "relevancy",  # Or 'popularity', 'publishedAt'
        }
        if sources:
            params["sources"] = sources  # Add sources to parameters if provided

        logger.info(f"Fetching news from NewsAPI for topic: '{topic}', sources: '{sources if sources else 'all'}'")
        response = requests.get(NEWSAPI_ENDPOINT, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()

        results = []
        if data.get("status") == "ok" and data.get("articles"):
            for article in data["articles"]:
                results.append({
                    "title": article.get("title", "No Title"),
                    "link": article.get("url", "#"),
                    "summary": article.get("description", "No Description"),  # Using description as summary
                    "source": article.get("source", {}).get("name", "Unknown Source")
                })
        logger.info(f"Successfully fetched {len(results)} articles from NewsAPI.")
        return results
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching from NewsAPI: {e}")
        return []
    except json.JSONDecodeError:
        logger.error("Error decoding JSON response from NewsAPI.")
        return []


def perform_scraping(topic, sources=None):
    """Orchestrates the scraping process (now just news)."""
    all_results = []

    # News from NewsAPI
    logger.info(f"Fetching news from NewsAPI for: {topic}, sources: {sources if sources else 'all'}")
    news_results = fetch_news_from_api(topic, sources=sources)
    all_results.extend(news_results)

    return all_results


@app.route('/api/scrape', methods=['GET'])  # API endpoint for scraping
def api_scrape():
    topic = request.args.get('topic')  # Get topic from query parameter
    sources_str = request.args.get('sources') # Get sources as a string parameter
    sources = sources_str.split(',') if sources_str else None # Split sources string into a list, or None if empty

    if not topic:
        return jsonify({"error": "Topic parameter is missing"}), 400  # Bad request if topic is missing

    results = perform_scraping(topic, sources=sources) # Pass sources to perform_scraping
    return jsonify(results)  # Return results as JSON


if __name__ == '__main__':
    logger.info("Starting Flask backend in debug mode...")
    app.run(debug=True, port=5000) # Run Flask backend on port 5000 (or any port you prefer)
