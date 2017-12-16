import requests
from datetime import datetime


config = {
    'VK_ACCESS_TOKEN': 'd05b1440a5d401e04b9872fc039d9129724e4bdcf55bc44c3429de2de26aa3fb13193bdc87752d89361e5',
    'PLOTLY_USERNAME': 'Имя пользователя Plot.ly',
    'PLOTLY_API_KEY': 'Ключ доступа Plot.ly'
}


def get(url, params={'user_id': 65000344, 'fields': 'sex'}, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос

    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    domain = url
    query_params = {
        'domain': domain,
        'access_token': config['VK_ACCESS_TOKEN'],
        'user_id': params['user_id'],
        'fields': params['fields'],
        'method': params['method']
    }

    query = "{domain}/{method}?access_token={access_token}&user_id={user_id}&fields={fields}&v=5.53".format(
        **query_params)
    response = requests.get(query)
    return response


def get_friends(user_id, fields):
    """ Вернуть данных о друзьях пользователя

    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    params = {
        'user_id': user_id,
        'fields': fields,
        'method': 'friends.get'
    }
    response = get("https://api.vk.com/method", params)
    return response


def age_predict(user_id):
    """ Наивный прогноз возраста по возрасту друзей

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: идентификатор пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    response = get_friends(user_id, 'bdate')
    print(response.json())
    for i in range(5):
        print(response.json()['response']['items'][i])
    count = response.json()['response']['count']
    age = 0
    for i in range(response.json()['response']['count']):
        if ('bdate' not in response.json()['response']['items'][i])\
                or len(response.json()['response']['items'][i]['bdate']) < 7:
            count -= 1
        else:
            age += bdate_parse(response.json()['response']['items'][i]['bdate'])
    return age // count


def bdate_parse(bdate):
    age = 2017-int(bdate.split(sep='.')[2])
    return age


def messages_get_history(user_id, offset=0, count=100):
    """ Получить историю переписки с указанным пользователем

    :param user_id: идентификатор пользователя, с которым нужно получить историю переписки
    :param offset: смещение в истории переписки
    :param count: число сообщений, которое нужно получить
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"
    domain = "https://api.vk.com/method"

    query_params = {
        'domain': domain,
        'access_token': config['VK_ACCESS_TOKEN'],
        'user_id': user_id,
        'method': 'messages.getHistory',
        'offset': offset,
        'count': count
    }

    query = "{domain}/{method}?access_token={access_token}&user_id={user_id}&offset={offset}&count={count}&v=5.53".format(
        **query_params)
    response = requests.get(query)
    print(response.json())
    return response.json()['response']


def count_dates_from_messages(messages):
    """ Получить список дат и их частот

    :param messages: список сообщений
    """
    from collections import Counter
    count = 100
    date_list = []
    for i in range(count):
        date_list.append(datetime.fromtimestamp(messages['items'][i]['date']).strftime("%Y-%m-%d"))
    return Counter(date_list)


def plotly_messages_freq(freq_dict):
    """ Построение графика с помощью Plot.ly

    :param freq_list: список дат и их частот
    """
    import plotly
    plotly.tools.set_credentials_file(username='9427', api_key='rWqlbcvoUiQ0biGrGNN3')
    date_list, date_freq = dict_split(freq_dict)
    data = [plotly.graph_objs.Scatter(x=date_list, y=date_freq)]
    plotly.plotly.plot(data)
    pass


def dict_split(freq_dict):
    #list1 = [freq_dict.keys[i] for i in sorted(freq_dict.keys())]
    #list2 = [freq_dict.values[i] for i in sorted(freq_dict.keys())]
    return list(freq_dict.keys()), list(freq_dict.values())


def graph_messages(user_id):
    messages = messages_get_history(user_id)
    freq_dict = count_dates_from_messages(messages)
    plotly_messages_freq(freq_dict)


def get_network(users_ids, as_edgelist=True):
    # PUT YOUR CODE HERE
    pass


def plot_graph(graph):
    # PUT YOUR CODE HERE
    pass


if __name__ == '__main__':
    #103435854
    #339123961
    #382652267
    graph_messages(103435854)
