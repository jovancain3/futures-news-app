from flask import Flask, render_template, request, jsonify
from duckduckgo_search import DDGS
from datetime import datetime

app = Flask(__name__)

def search_news(query, max_results=5):
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, region='wt-wt', safesearch='Moderate', max_results=max_results):
            results.append({
                'title': r['title'],
                'url': r['href']
            })
    return results

@app.route('/')
def home():
    today = datetime.now().strftime("%B %d, %Y")
    return render_template('index.html', today=today)

@app.route('/get_futures_news')
def get_futures_news():
    query = "latest futures market news"
    news = search_news(query)
    return jsonify({'news': news})

@app.route('/search_currency')
def search_currency():
    currency = request.args.get('currency', '').strip()
    if not currency:
        return jsonify({'error': 'Currency input is required.'})
    
    query = f"{currency} currency news latest"
    news = search_news(query)
    return jsonify({'news': news})

if __name__ == '__main__':
    app.run(debug=True)
