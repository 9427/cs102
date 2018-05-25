from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session
from not_bayes import ProbablyNotBayesClassifier
from not_bayes import clean, random_score


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/news/labeled")
def labeled_news_list():
    s = session()
    rows = s.query(News).filter(News.label != None).all()
    sorted_rows = []
    for i in range(5, 0, -1):
        for row in rows:
            if row.label == i:
                sorted_rows.append(row)
    return template('labeled_news_template', rows=sorted_rows)


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
    i = 0
    for data in news_dict:
        i += 1
        if s.query(News).filter(News.title == data['title']) or i > 150:
            print('boop')
        if i > 150:
            break
        news = News(title=data['title'], author=data['author'], url=data['url'], comments=data['comments'],
                     points=data['points'])
        s.add(news)
        s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    s = session()
    model = ProbablyNotBayesClassifier()
    x_data = s.query(News.title).filter(News.label != None).all()
    x_data = [clean(x[0]) for x in x_data]
    y_data = [int(y[0]) for y in s.query(News.label).filter(News.label != None).all()]
    split_range = round(len(x_data) * 0.7)
    x_train, y_train, x_test, y_test = x_data[:split_range], y_data[:split_range], x_data[split_range:], y_data[split_range:]
    #x_data = s.query(News).filter(News.label == None).all()
    model.train(x_train, y_train)
    #for data in x_test:
    #    clean_data = clean(data.title)
    #    data.label = model.predict(clean_data)
    print(model.score(x_test, y_test))
    print(random_score(x_test, y_test))
    redirect("/news/labeled")

@route("/classify/bayes")
def classify_bayes():
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.pipeline import Pipeline
    from sklearn.feature_extraction.text import TfidfVectorizer

    s = session()
    model = Pipeline([
        ('vectorizer', TfidfVectorizer()),
        ('classifier', MultinomialNB(alpha=0.05)),
    ])
    x_data = s.query(News.title).filter(News.label != None).all()
    x_data = [clean(x[0]) for x in x_data]
    y_data = [int(y[0]) for y in s.query(News.label).filter(News.label != None).all()]
    split_r = round(len(x_data) * 0.3)
    x_test, y_test, x_train, y_train = x_data[:split_r], y_data[:split_r], x_data[split_r:], y_data[split_r:]
    model.fit(x_train, y_train)
    print(model.score(x_test, y_test))
    redirect("/news/labeled")
                                  

if __name__ == "__main__":
    run(host="localhost", port=8080)
    

