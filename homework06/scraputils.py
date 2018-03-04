import requests
from bs4 import BeautifulSoup
import re


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    user_list = parser.select(".hnuser")
    sub_list = parser.select(".subtext")
    article_list = parser.select(".storylink")
    for i in range(30):
        if sub_list[i].findAll('a')[3].string == 'discuss':
            sub_list[i].findAll('a')[3].string = '0 comments'
        data = {
            'author': user_list[i].string,
            'comments': int(re.search(r'\d+', sub_list[i].findAll('a')[3].string).group()),
            'points': int(re.search(r'\d+', sub_list[i].find('span').string).group()),
            'title': article_list[i].string,
            'url': article_list[i].get('href')
        }
        news_list.append(data)
    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    # PUT YOUR CODE HERE


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    #print(soup)
    news_list = extract_news(soup)
    '''while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1'''


    return news_list

if __name__ == "__main__":
    print(get_news('https://news.ycombinator.com/'))
