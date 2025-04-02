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

    api_key = ''  # 무료 Microlink 키 (비워두면 무료 제한 적용)
    microlink_api = f"https://api.microlink.io/?url={url}&prerender=true&data.html=true"

    headers = {'x-api-key': api_key} if api_key else {}
    response = requests.get(microlink_api, headers=headers)
    data = response.json()

    if 'data' not in data or 'html' not in data['data']:
        return jsonify([])

    html = data['data']['html']
    soup = BeautifulSoup(html, "html.parser")

    articles = []
    # 명시적으로 CSS Selector 조정 (OpenAI 실제 페이지 구조에 맞춤)
    for link in soup.select('a[href^="/research/"]'):
        title_element = link.select_one('h3, h4, span')
        title = title_element.text.strip() if title_element else "제목 없음"
        href = link['href']
        full_link = f"https://openai.com{href}"
        articles.append({"title": title, "link": full_link})

    # 중복 제거
    seen = set()
    unique_articles = []
    for article in articles:
        if article['link'] not in seen:
            unique_articles.append(article)
            seen.add(article['link'])

    return jsonify(unique_articles[:30])

if __name__ == "__main__":
    app.run()
