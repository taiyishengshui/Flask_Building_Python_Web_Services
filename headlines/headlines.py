# /usr/bin/python3
import feedparser
from flask import Flask, render_template
from flask import request
import requests
import urllib.parse

app = Flask(__name__)

RSS_FEEDS = {
    'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
    'fox': 'http://feeds.foxnews.com/foxnews/latest',
    'iol': 'http://www.iol.co.za/cmlink/1.640'
}

DEFAULTS={
    'publication':'bbc',
    'city':'北京'
}

# @app.route("/", methods=['GET', 'POST'])
@app.route("/")
def home():
    publication = request.args.get('publication')
    if not publication:
        publication=DEFAULTS['publication']
    articles = get_news(publication)
    city = request.args.get('city')
    if not city:
        city = DEFAULTS['city']
    # print(city)
    weather = get_weather(city)
    return render_template("home.html", articles=articles,weather=weather)
def get_news(query):
    # query = str(request.args.get("publication"))
    # print("query",query.lower())
    if not query or query.lower() not in RSS_FEEDS:
        publication = "bbc"
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']

def get_weather(query):
    # api_url="http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=a567483dd49d04a2a38bfe331ba79803"
    # # query = urllib.parse.unquote(query)
    # # print(type(query))
    # url = api_url.format(query)
    # print(url)
    # data = requests.get(url)
    # parsed = data.json()
    # weather = None
    # print(parsed.get("weather"))
    # if parsed.get("weather"):
    #     weather = {
    #         "description":parsed["weather"][0]["description"],
    #         "temperature":parsed["main"]["temp"],
    #         "city":parsed["name"]
    #     }
    api_url = "https://www.sojson.com/open/api/weather/json.shtml?city={}"
    query = urllib.parse.unquote(query)
    url = api_url.format(query)
    data = requests.get(url)
    parsed = data.json()
    weather = None
    # print(parsed)
    if parsed:
        weather = {
            "city":parsed['city'],
            "description":parsed['data']['forecast'][0]['type'],
            "temperature":parsed['data']['wendu']
        }
    return weather


# @app.route("/<publication>")
# def get_news(publication="bbc"):
#   feed = feedparser.parse(RSS_FEEDS[publication])
#    first_article = feed['entries'][0]
#  return render_template("home.html",articles=feed['entries'])

if __name__ == '__main__':
    app.run(port=5000, debug=True)


# def get_news():
#     query = str(request.form.get("publication"))
#     # print("query=", query.lower())
#     if not query:
#         publication = "bbc"
#     elif query.lower() not in RSS_FEEDS:
#         publication = "bbc"
#     else:
#         publication = query.lower()
#     # print("publicatio=",publication)
#     # print(RSS_FEEDS[publication])
#     feed = feedparser.parse(RSS_FEEDS[publication])
#     # print(feed)
#     return render_template("home.html", articles=feed['entries'])
