import requests
from datetime import datetime


config = {
    'VK_ACCESS_TOKEN': 'Tокен доступа для ВК',
    'PLOTLY_USERNAME': 'Имя пользователя Plot.ly',
    'PLOTLY_API_KEY': 'Ключ доступа Plot.ly'
}


def get(url, params={}, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос

    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    domain = "https://api.vk.com/method"
    access_token = "fca60a3410223b4d5ba0bc5ac624f20e5d91e33639d397e9dc3ac7a37d412ef69a17b90a21e381f43efab"
    user_id = 65000344

    query_params = {
        'domain': domain,
        'access_token': access_token,
        'user_id': user_id,
        'fields': 'age'
    }

    query = "{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v=5.53".format(
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
    # PUT YOUR CODE HERE


def age_predict(user_id):
    """ Наивный прогноз возраста по возрасту друзей

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: идентификатор пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    # PUT YOUR CODE HERE


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
    # PUT YOUR CODE HERE


def count_dates_from_messages(messages):
    """ Получить список дат и их частот

    :param messages: список сообщений
    """
    # PUT YOUR CODE HERE


def plotly_messages_freq(freq_list):
    """ Построение графика с помощью Plot.ly

    :param freq_list: список дат и их частот
    """
    # PUT YOUR CODE HERE
    pass

def get_network(users_ids, as_edgelist=True):
    # PUT YOUR CODE HERE
    pass


def plot_graph(graph):
    # PUT YOUR CODE HERE
    pass

if __name__ == '__main__':
    response = get("https://api.vk.com/method")
    print(response.json())