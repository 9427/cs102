import requests
from datetime import datetime


config = {
    'VK_ACCESS_TOKEN': 'd05b1440a5d401e04b9872fc039d9129724e4bdcf55bc44c3429de2de26aa3fb13193bdc87752d89361e5',
    'DOMAIN': 'https://api.vk.com/method'
}


def get(params={'user_id': 65000344, 'fields': 'sex'}, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос

    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    query_params = {
        'domain': config['DOMAIN'],
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
    response = get(params)
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

    query_params = {
        'domain': config['DOMAIN'],
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

    :param freq_dict: словарь дат и их частот
    """
    import plotly
    plotly.tools.set_credentials_file(username='9427', api_key='rWqlbcvoUiQ0biGrGNN3')
    date_list, date_freq = dict_split(freq_dict)
    data = [plotly.graph_objs.Scatter(x=date_list, y=date_freq)]
    plotly.plotly.plot(data)
    pass


def dict_split(freq_dict):
    # list1 = [freq_dict.keys[i] for i in sorted(freq_dict.keys())]
    # list2 = [freq_dict.values[i] for i in sorted(freq_dict.keys())]
    return list(freq_dict.keys()), list(freq_dict.values())


def graph_messages(user_id):
    messages = messages_get_history(user_id)
    freq_dict = count_dates_from_messages(messages)
    plotly_messages_freq(freq_dict)


def get_mutual_friends(user_id, fields, target_id):
    """ Returns a list of user IDs or detailed information about a user's friends """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(target_id, int), "target_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    assert target_id > 0, "target_id must be positive integer"

    query_params = {
        'domain': config['DOMAIN'],
        'access_token': config['VK_ACCESS_TOKEN'],
        'user_id': user_id,
        'method': 'friends.getMutual',
        'fields': fields,
        'target_id': target_id
    }

    query = "{domain}/{method}?access_token={access_token}&user_id={user_id}&fields={fields}&target_uid={target_id}&v=5.53".format(
        **query_params)
    response = requests.get(query)
    return response.json()


def get_network(user_ids, as_edgelist=True):
    # PUT YOUR CODE HERE
    pass


def plot_graph(graph=1):
    import igraph
    from jgraph import Graph, plot

    vertices = [i for i in range(7)]
    edges = [
        (0, 2), (0, 1), (0, 3),
        (1, 0), (1, 2), (1, 3),
        (2, 0), (2, 1), (2, 3), (2, 4),
        (3, 0), (3, 1), (3, 2),
        (4, 5), (4, 6),
        (5, 4), (5, 6),
        (6, 4), (6, 5)
    ]

    g = Graph(vertex_attrs={"label": vertices},
              edges=edges, directed=False)
    N = len(vertices)
    visual_style = {}
    visual_style["layout"] = g.layout_fruchterman_reingold(
        maxiter=1000,
        area=N ** 3,
        repulserad=N ** 3)
    # g.simplify(multiple=True, loops=True)
    # communities = g.community_edge_betweenness(directed=False)
    # clusters = communities.as_clustering()
    # pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    # g.vs['color'] = pal.get_many(clusters.membership)
    plot(g, **visual_style)
    pass


if __name__ == '__main__':
    #103435854
    #339123961
    #382652267
    #print(get_mutual_friends(65000344, '', 103435854))
    plot_graph()
