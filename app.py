from flask import Flask, jsonify
from requests_html import HTMLSession

app = Flask(__name__)

@app.route('/crawl-openai')
def crawl_openai():
    session = HTMLSession()
    url = "https://openai.com/research"
    response = session.get(url)
    response.html.render(sleep=3)

    articles = []
    for link in response.html.find('a[href^="/research/"]'):
        title_element = link.find('span,h2,h3', first=True)
        if title_element:
            title = title_element.text
            href = link.attrs['href']
            articles.append({"title": title, "link": f"https://openai.com{href}"})

    unique_articles = [dict(t) for t in {tuple(d.items()) for d in articles}]
    return jsonify(unique_articles[:30])

if __name__ == "__main__":
    app.run()
