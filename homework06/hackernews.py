from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session
from not_bayes import NaiveBayesClassifier
from not_bayes import clean


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/news/labeled")
def labeled_news_list():
    s = session()
    rows = s.query(News).filter(News.label != None).all()
    return template('labeled_news_template', rows=rows)


@route("/add_label/")
def add_label():
    id, label = request.query.id, request.query.label
    s = session()
    article = s.query(News).filter(News.id == id).all()[0]
    article.label = label
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    s = session()
    news_dict = get_news('https://news.ycombinator.com/')
    for data in news_dict:
        if s.query(News).filter(News.title == data['title']):
            break
        news = News(title=data['title'], author=data['author'], url=data['url'], comments=data['comments'],
                     points=data['points'])
        s.add(news)
        s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    s = session()
    model = NaiveBayesClassifier()
    x_train = s.query(News.title).filter(News.label != None).all()
    x_train = [clean(x[0]) for x in x_train]
    y_train = [int(y[0]) for y in s.query(News.label).filter(News.label != None).all()]
    model.train(x_train, y_train)
    x_data = s.query(News).filter(News.label == None).all()
    for data in x_data:
        clean_data = clean(data.title)
        data.label = model.predict(clean_data)
    sorted_rows = []
    for i in range(5, 0, -1):
        for row in x_data:
            if row.label == i:
                sorted_rows.append(row)
    return template('labeled_news_template', rows=sorted_rows)

if __name__ == "__main__":
    run(host="localhost", port=8080)

