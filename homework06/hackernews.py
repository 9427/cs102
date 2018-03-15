from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session
#from bayes import NaiveBayesClassifier


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():

    redirect("/news")


@route("/update")
def update_news():
    s = session()
    news_dict = get_news('https://news.ycombinator.com/')
    for data in news_dict:
        if not s.query(News).filter(News.title == data['title']):
            break
        news = News(title=data['title'], author=data['author'], url=data['url'], comments=data['comments'],
                     points=data['points'])
        s.add(news)
        s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    # PUT YOUR CODE HERE
    return 0

if __name__ == "__main__":
    run(host="localhost", port=8080)

