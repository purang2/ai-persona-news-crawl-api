from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "AI Persona News API Running!"})

@app.route('/crawl-openai')
def crawl_openai():
    microlink_api = "https://api.microlink.io/"
    url = "https://openai.com/research"

    response = requests.get(microlink_api, params={"url": url, "prerender": "true"})
    data = response.json()

    if 'data' not in data or 'links' not in data['data']:
        return jsonify([])

    articles = []
    for link in data['data']['links']:
        if "/research/" in link['url']:
            articles.append({
                "title": link.get("title", "제목 없음"),
                "link": link['url']
            })

    return jsonify(articles[:30])

if __name__ == "__main__":
    app.run()
