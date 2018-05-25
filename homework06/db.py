from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
engine = create_engine("sqlite:///news.db")
session = sessionmaker(bind=engine)
s = session()


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(Integer)


'''Base.metadata.create_all(bind=engine)
news_dict = get_news('https://news.ycombinator.com/')
for data in news_dict:
    news = News(title=data['title'], author=data['author'], url=data['url'], 
    comments=data['comments'], points=data['points'])
    s.add(news)
    s.commit()'''
