from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# 경로 1: OpenAI Research 크롤링
@app.route('/crawl-openai')
def crawl_openai():
    res = requests.get("https://openai.com/research")
    soup = BeautifulSoup(res.text, 'html.parser')

    articles = []
    for post in soup.select('a[href^="/research/"]')[:30]:
        title = post.get_text(strip=True)
        link = 'https://openai.com' + post['href']
        articles.append({'title': title, 'link': link})

    return jsonify(articles)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
