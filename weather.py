import feedparser

def get_news():
    urls= "http://news.ifeng.com/rss/index.xml"
    # query = str(request.args.get("publication"))
    # print("query",query.lower())
    feed = feedparser.parse(urls)
    articles =feed['entries']
    for article in articles:
        print(article.link)

get_news()