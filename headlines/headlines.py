# /usr/bin/python3
import feedparser
from flask import Flask, render_template, make_response
from flask import request
import requests
import datetime
import urllib.parse

app = Flask(__name__)

RSS_FEEDS = {
    'qq': 'http://news.qq.com/newsgn/rss_newsgn.xml',
    'ft': 'http://www.ftchinese.com/rss/news',
    'ifeng': 'http://news.ifeng.com/rss/index.xml'
}

DEFAULTS = {
    'publication': 'ifeng',
    'city': 'beijing,cn',
    'currency_from': 'CNY',
    'currency_to': 'USD',

}

WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=a567483dd49d04a2a38bfe331ba79803"
CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id=aec14afce2de44d0b37d56d171675ec8"


def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]


# @app.route("/", methods=['GET', 'POST'])
@app.route("/")
def home():
    # get customised headlines, based on user input or default
    publication = get_value_with_fallback("publication")

    # get customised weather based on user input or default
    articles = get_news(publication)
    city = get_value_with_fallback("city")
    weather = get_weather(city)

    # get customised currency based on user input or default
    currency_from = get_value_with_fallback("currency_from")
    currency_to = get_value_with_fallback("currency_to")
    rate, currencies = get_rates(currency_from, currency_to)

    # save cookies and return template
    response = make_response(render_template("home.html",
                                             articles=articles,
                                             weather=weather,
                                             currency_from=currency_from,
                                             currency_to=currency_to,
                                             rate=rate,
                                             currencies=sorted(currencies)))
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie("publication", publication, expires=expires)
    response.set_cookie("city", city, expires=expires)
    response.set_cookie("currency_from", currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)
    return response


def get_rates(frm, to):
    all_currency = requests.get(CURRENCY_URL)
    parsed = all_currency.json()['rates']
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return (to_rate / frm_rate, parsed.keys())


def get_news(query):
    # query = str(request.args.get("publication"))
    # print("query",query.lower())
    if not query or query.lower() not in RSS_FEEDS:
        publication = "ft"
    else:
        publication = query.lower()
    print(RSS_FEEDS[publication])
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']


def get_weather(query):
    # api_url="http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=a567483dd49d04a2a38bfe331ba79803"
    # query = urllib.parse.unquote(query)
    # print(type(query))
    url = WEATHER_URL.format(query)

    data = requests.get(url)
    parsed = data.json()
    weather = None
    if parsed.get("weather"):
        weather = {
            "description": parsed["weather"][0]["description"],
            "temperature": parsed["main"]["temp"],
            "city": parsed["name"],
            "country": parsed["sys"]["country"],
        }
    return weather

    # 国内api
    # api_url = "https://www.sojson.com/open/api/weather/json.shtml?city={}"
    # query = urllib.parse.unquote(query)
    # url = api_url.format(query)
    # data = requests.get(url)
    # parsed = data.json()
    # weather = None
    # # print(parsed)
    # if parsed:
    #     weather = {
    #         "city": parsed['city'],
    #         "pm25": parsed['data']['pm25'],
    #         "description": parsed['data']['forecast'][0]['type'],
    #         "temperature": parsed['data']['wendu'],
    #         "notice": parsed['data']['forecast'][0]['notice']
    #     }
    # return weather


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


# old home
# def home():
#     publication = request.args.get('publication')
#     if not publication:
#         publication = DEFAULTS['publication']
#     articles = get_news(publication)
#     city = request.args.get('city')
#     if not city:
#         city = DEFAULTS['city']
#     # print(city)
#     weather = get_weather(city)
#     currency_from = request.args.get("currency_from")
#     if not currency_from:
#         currency_from = DEFAULTS['currency_from']
#     currency_to = request.args.get("currency_to")
#     if not currency_to:
#         currency_to = DEFAULTS['currency_to']
#     rate, currencies = get_rates(currency_from, currency_to)
#     # rate = get_rates(currency_from, currency_to)
#     return render_template("home.html", articles=articles, weather=weather,
#                            currency_from=currency_from, currency_to=currency_to, rate=rate,
#                            currencies=sorted(currencies))
