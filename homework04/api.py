import requests
from datetime import datetime


config = {
    'VK_ACCESS_TOKEN': 'b25bab4e1d96a2990cfa0dacfae0d51de9c7620371af1ea03af6d4f77aa58cba004f1af23006d2c119088',
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
#age = sum(bdate_parse(s['bdate']) for s in response.json()['response']['items'] if len(s['bdate']) < 7)


def messages_get_history(user_id, offset=0, count=20):
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
    access_token = "5fdea00c123047bc2061ed021786b468da03b979114c4465522e7dc10f2789b06adf53a318c6180d0cea9"

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
    return response


def count_dates_from_messages(messages):
    """ Получить список дат и их частот

    :param messages: список сообщений
    """
    from collections import Counter

    messages_get_history(user_id)
    count = messages['count']
    date_list = []
    for i in range(count):
        date_list.append(datetime.fromtimestamp(messages['items'][i]['date']).strftime("%Y-%m-%d"))
    return Counter(date_list)

def plotly_messages_freq(freq_dict):
    """ Построение графика с помощью Plot.ly

    :param freq_list: список дат и их частот
    """
    import plotly

    plotly.tools.set_credentials_file(username='', api_key='')
    messages = messages_get_history(user_id='65000344')
    freq_dict = count_dates_from_messages(messages)
    date_list, date_freq = dict_split(freq_dict)
    data = [plotly.graph_objs.Scatter(x=date_list, y=date_freq)]
    plotly.plotly.plot(data)
    pass


def get_network(users_ids, as_edgelist=True):
    # PUT YOUR CODE HERE
    pass


def plot_graph(graph):
    # PUT YOUR CODE HERE
    pass


def bdate_parse(bdate):
    age = 2017-int(bdate.split(sep='.')[2])
    return age


def dict_split(freq_dict):
    list1 = [freq_dict.keys[i] for i in sorted(freq_dict.keys())]
    list2 = [freq_dict.values[i] for i in sorted(freq_dict.keys())]
    return list1, list2

if __name__ == '__main__':
    responses = messages_get_history(740914)
    print(responses.json())