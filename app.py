from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "AI Persona News API Running!"})

@app.route('/crawl-openai')
def crawl_openai():
    url = "https://openai.com/research"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    articles = []
    for link in soup.select('a[href^="/research/"]'):
        title_element = link.select_one('span, h2, h3')
        if title_element:
            title = title_element.get_text(strip=True)
            href = link['href']
            articles.append({"title": title, "link": f"https://openai.com{href}"})

    # 중복 제거 및 최대 30개 제한
    seen = set()
    unique_articles = []
    for article in articles:
        if article['link'] not in seen:
            unique_articles.append(article)
            seen.add(article['link'])
        if len(unique_articles) >= 30:
            break

    return jsonify(unique_articles)

if __name__ == "__main__":
    app.run()
