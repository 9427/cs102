import requests
from bs4 import BeautifulSoup
import re


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    user_list = parser.select(".hnuser")
    sub_list = parser.select(".subtext")
    article_list = parser.select(".storylink")
    err_num = 0
    for i in range(30):
        try:
            if sub_list[i].findAll('a')[3].string == 'discuss':
                sub_list[i].findAll('a')[3].string = '0 comments'
            data = {
                'author': user_list[i].string,
                'comments': int(re.search(r'\d+', sub_list[i].findAll('a')[3].string).group()),
                'points': int(re.search(r'\d+', sub_list[i].find('span').string).group()),
                'title': article_list[i].string,
                'url': article_list[i].get('href')
            }
            if data['url'].find('item?id=') == 0:
                data['url'] = 'https://news.ycombinator.com/' + data['url']
            news_list.append(data)
        except:
            print('Error parsing article', err_num + len(news_list))
            err_num += 1
    return news_list


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    next_page = 'news?p=1'
    n_pages = 20
    for i in range(2, n_pages + 2):
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = 'news?p=' + str(i)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
    return news

if __name__ == "__main__":
    print(get_news('https://news.ycombinator.com/'))
