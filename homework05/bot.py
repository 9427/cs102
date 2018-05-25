import datetime
import requests
import telebot
import time
from bs4 import BeautifulSoup

config = {
    'access-token': '501843166:AAHihi2TwdWucnR2x-PfD-uLwN4k9njSdXI',
    'domain': 'http://www.ifmo.ru/ru/schedule/0'
}

bot = telebot.TeleBot(config['access-token'])


def get_page(week='', group='K3142'):
    if week:
        week = str(week) + '/'
    if week == '0/':
        week = ''
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config['domain'],
        week=week,
        group=group
    )
    response = requests.get(url)
    web_page = response.text
    return web_page


def get_schedule(web_page, day):
    soup = BeautifulSoup(web_page, "html5lib")
    if day == '/monday' or day == '/sunday':
        schedule_table = soup.find("table", attrs={"id": "1day"})
    elif day == '/tuesday':
        schedule_table = soup.find("table", attrs={"id": "2day"})
    elif day == '/wednesday':
        schedule_table = soup.find("table", attrs={"id": "3day"})
    elif day == '/thursday':
        schedule_table = soup.find("table", attrs={"id": "4day"})
    elif day == '/friday':
        schedule_table = soup.find("table", attrs={"id": "5day"})
    elif day == '/saturday':
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


@bot.message_handler(commands=['all'])
def get_week(message):
    if len(message.text.split()) != 1:
        _, group, week = message.text.split()
        web_page = get_page(week, group)
        if int(week) == 1:
            resp = '<b>Расписание на четную неделю:</b>\n'
        elif int(week) == 2:
            resp = '<b>Расписание на нечетную неделю:</b>\n'
        elif int(week) == 0:
            resp = '<b>Общее расписание:</b>\n'
    week_list = ['/monday', '/tuesday', '/wednesday', '/thursday', '/friday', '/saturday']
    week_name_list = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
    for i in range(6):
        resp += '<b>' + week_name_list[i] + '</b>' + ':\n'
        schedule = get_schedule(web_page, week_list[i])
        if not schedule:
            bot.send_message(message.chat.id, 'Ошибка, возможно, занятий нет?')
            return None

        times_list, locations_list, lessons_list = schedule

        for time, location, lesson in zip(times_list, locations_list, lessons_list):
            resp += '<b>{}</b>, {}, {}\n'.format(time, location, lesson)
        resp += '\n'
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['tomorrow'])
def get_tomorrow(message):
    _, group = message.text.split()
    if int(datetime.datetime.today().strftime('%U')) % 2 == 1:
        week = '2'
    else:
        week = '1'
    web_page = get_page(week, group)
    today = datetime.datetime.now()
    tomorrow = today
    if today.weekday() == 5:
        tomorrow += datetime.timedelta(days=2)
    else:
        tomorrow += datetime.timedelta(days=1)
    if tomorrow.weekday() == 0:
        tomorrow = '/monday'
    elif tomorrow.weekday() == 1:
        tomorrow = '/tuesday'
    elif tomorrow.weekday() == 2:
        tomorrow = '/wednesday'
    elif tomorrow.weekday() == 3:
        tomorrow = '/thursday'
    elif tomorrow.weekday() == 4:
        tomorrow = '/friday'
    elif tomorrow.weekday() == 5:
        tomorrow = '/saturday'
    schedule = get_schedule(web_page, tomorrow)
    if not schedule:
        bot.send_message(message.chat.id, 'Ошибка')
        return None

    times_list, locations_list, lessons_list = schedule
    resp = '<b>Расписание на завтра:\n</b>'
    for time, location, lesson in zip(times_list, locations_list, lessons_list):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lesson)

    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_day(message):
    day, group, week = message.text.split()
    web_page = get_page(week, group)
    schedule = get_schedule(web_page, day)
    if not schedule:
        bot.send_message(message.chat.id, 'Ошибка, возможно, занятий нет?')
        return
    times_list, locations_list, lessons_list = schedule
    resp = ''
    for time, location, lesson in zip(times_list, locations_list, lessons_list):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lesson)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['near'])
def get_next_lesson(message):
    _, group = message.text.split()
    today = datetime.datetime.now().weekday()
    if today != 6:
        if today == 0:
            today = '/monday'
        elif today == 1:
            today = '/tuesday'
        elif today == 2:
            today = '/wednesday'
        elif today == 3:
            today = '/thursday'
        elif today == 4:
            today = '/friday'
        elif today == 5:
            today = '/saturday'
    else:
        bot.send_message(message.chat.id, 'Ошибка, возможно, занятий нет?')
    if int(datetime.datetime.today().strftime('%U')) % 2 == 1:
        week = '2'
    else:
        week = '1'
    web_page = get_page(week, group)
    schedule = get_schedule(web_page, today)
    if not schedule:
        bot.send_message(message.chat.id, 'Ошибка, возможно, занятий нет?')
        return None
    times_list, locations_list, lessons_list = schedule
    j = 0
    state = 0
    for i in times_list:
        time, _ = i.split('-')
        t1, t2 = time.split(':')
        time = int(t1 + t2)
        cur_time = int(str(datetime.datetime.now().hour) + str(datetime.datetime.now().minute))
        if cur_time < time:
            resp = '<b>Ближайшая пара сегодня:</b>\n'
            resp += '<b>{}</b>, {}, {}\n'.format(times_list[j], locations_list[j], lessons_list[j])
            bot.send_message(message.chat.id, resp, parse_mode='HTML')
            state = 1
            break
        j += 1
    if not state:
        today = datetime.datetime.now()
        tomorrow = today
        if today.weekday() == 5:
            tomorrow += datetime.timedelta(days=2)
        else:
            tomorrow += datetime.timedelta(days=1)
        schedule = False
        while not schedule:
            if tomorrow.weekday() == 0:
                schedule = get_schedule(web_page, '/monday')
                if not schedule:
                    tomorrow += datetime.timedelta(days=1)
            elif tomorrow.weekday() == 1:
                schedule = get_schedule(web_page, '/tuesday')
                if not schedule:
                    tomorrow += datetime.timedelta(days=1)
            elif tomorrow.weekday() == 2:
                schedule = get_schedule(web_page, '/wednesday')
                if not schedule:
                    tomorrow += datetime.timedelta(days=1)
            elif tomorrow.weekday() == 3:
                schedule = get_schedule(web_page, '/thursday')
                if not schedule:
                    tomorrow += datetime.timedelta(days=1)
            elif tomorrow.weekday() == 4:
                schedule = get_schedule(web_page, '/friday')
                if not schedule:
                    tomorrow += datetime.timedelta(days=1)
            elif tomorrow.weekday() == 5:
                schedule = get_schedule(web_page, '/saturday')
                if not schedule:
                    tomorrow += datetime.timedelta(days=1)
        day_next = ''
        if tomorrow.weekday() == 0:
            day_next += 'Понедельник'
        elif tomorrow.weekday() == 1:
            day_next += 'Вторник'
        elif tomorrow.weekday() == 2:
            day_next += 'Среда'
        elif tomorrow.weekday() == 3:
            day_next += 'Четверг'
        elif tomorrow.weekday() == 4:
            day_next += 'Пятница'
        elif tomorrow.weekday() == 5:
            day_next += 'Суббота'
        times_list, locations_list, lessons_list = schedule
        resp = '<b>Ближайшая пара (' + day_next + '):</b>\n'
        resp += '<b>{}</b>, {}, {}\n'.format(times_list[0], locations_list[0], lessons_list[0])
        bot.send_message(message.chat.id, resp, parse_mode='HTML')


while True:
    try:
        bot.polling(none_stop=True)
    except:
        time.sleep(5)
