from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "AI Persona News API Running!"})

@app.route('/crawl-openai')
def crawl_openai():
    try:
        res = requests.get("https://openai.com/research")
        soup = BeautifulSoup(res.text, 'html.parser')

        articles = []
        for link in soup.select('a[href^="/research/"]'):
            title_element = link.select_one('h3, h4, span')
            title = title_element.text.strip() if title_element else "제목 없음"
            href = link.get('href')
            if href:
                articles.append({
                    "title": title,
                    "link": f"https://openai.com{href}"
                })

        if not articles:
            return jsonify({"error": "No articles found."}), 500

        unique_articles = [dict(t) for t in {tuple(d.items()) for d in articles}]
        return jsonify(unique_articles[:30])

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
