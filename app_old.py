from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import time
import random
from concurrent.futures import ThreadPoolExecutor
import urllib.parse

app = Flask(__name__)

# Simplified to just use Google
SEARCH_ENGINE = "https://www.google.com/search?q="

# Financial news sources
FINANCIAL_SOURCES = [
    "site:reuters.com",
    "site:bloomberg.com",
    "site:ft.com",
    "site:wsj.com",
    "site:marketwatch.com",
    "site:investing.com",
    "site:forexlive.com",
    "site:fxstreet.com"
]

# User agent rotation to avoid getting blocked
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
]

# Function to get a random user agent
def get_random_user_agent():
    return random.choice(USER_AGENTS)

# Function to get news from different search engines
def get_news_from_engine(query, engine):
    try:
        # Format the search URL
        search_url = f"{engine}{urllib.parse.quote(query)}"
        
        # Add headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Make the request
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        
        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all search result links
        results = []
        for div in soup.find_all('div', class_='g'):
            link = div.find('a')
            if link and link.get('href'):
                url = link.get('href')
                if url.startswith('http'):  # Only include actual URLs
                    results.append(url)
        
        return results[:5]  # Return top 5 results
        
    except Exception as e:
        print(f"Error fetching news: {str(e)}")
        return []

# Function to fetch news
def fetch_news(query):
    search_query = f"{query} futures market financial news today"
    return get_news_from_engine(search_query, SEARCH_ENGINE)

# Function to fetch currency-specific news
def fetch_currency_news(currency):
    search_query = f"{currency} currency forex futures news today"
    return get_news_from_engine(search_query, SEARCH_ENGINE)

# Routes
@app.route('/')
def home():
    today = datetime.now().strftime("%B %d, %Y")
    return render_template('index.html', today=today)

@app.route('/get_futures_news')
def get_futures_news():
    news = fetch_news("futures market")
    return jsonify({"news": news})

@app.route('/search_currency')
def search_currency():
    currency = request.args.get('currency', '').strip()
    if not currency:
        return jsonify({"error": "Please enter a currency code or name"})
    
    news = fetch_currency_news(currency)
    return jsonify({"news": news})

if __name__ == '__main__':
    app.run(debug=True)