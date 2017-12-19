import requests
import telebot
from bs4 import BeautifulSoup


config = {
    'access_token': '501843166:AAHihi2TwdWucnR2x-PfD-uLwN4k9njSdXI',
    'domain': 'http://www.ifmo.ru/ru/schedule/0'
}

bot = telebot.TeleBot(config['access_token'])


def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config['domain'],
        week=week,
        group=group)
    response = requests.get(url)
    web_page = response.text
    return web_page


def parse_schedule_for_a_monday(web_page):
    soup = BeautifulSoup(web_page, "html5lib")

    # Получаем таблицу с расписанием на понедельник
    schedule_table = soup.find("table", attrs={"id": "2day"})

    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    return times_list, locations_list, lessons_list


# @bot.message_handler(commands=['monday'])
def get_monday(message):
    """ Получить расписание на понедельник """
    _, group = message.text.split()
    web_page = get_page(group)
    times_lst, locations_lst, lessons_lst = \
        parse_schedule_for_a_monday(web_page)
    resp = ''
    for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lesson)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message):
    """ Получить расписание на указанный день """
    day, group = message.text.split()
    web_page = get_page(group)
    soup = BeautifulSoup(web_page, "html5lib")
    if day == '/monday' or day == '/sunday' or day == '/Monday' or day == '/Sunday':
        schedule_table = soup.find("table", attrs={"id": "1day"})
    elif day == '/tuesday' or day == '/Tuesday':
        schedule_table = soup.find("table", attrs={"id": "2day"})
    elif day == '/wednesday' or day == '/Wednesday':
        schedule_table = soup.find("table", attrs={"id": "3day"})
    elif day == '/thursday' or day == '/Thursday':
        schedule_table = soup.find("table", attrs={"id": "4day"})
    elif day == '/friday' or day == '/Friday':
        schedule_table = soup.find("table", attrs={"id": "5day"})
    elif day == '/saturday' or day == '/Saturday':
        schedule_table = soup.find("table", attrs={"id": "6day"})
    if not schedule_table:
        return None
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.replace('\n', '').replace('\t', '') for lesson in lessons_list]
    return times_list, locations_list, lessons_list


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    # PUT YOUR CODE HERE
    pass


@bot.message_handler(commands=['tommorow'])
def get_tomorrow(message):
    """ Получить расписание на следующий день """
    # PUT YOUR CODE HERE
    pass


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    # PUT YOUR CODE HERE
    pass


if __name__ == '__main__':
    bot.polling(none_stop=True)