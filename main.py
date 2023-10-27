import keyboard as kb #Импорт наших клавиатур
from telebot import TeleBot #Импорт телебота
from googletrans import Translator #Импорт гугл переводчика
import pyjokes #Импорт шуточек
import requests #Парсинг
import json #удобный json
from currency_converter import CurrencyConverter #Перевод валют

#Токен бота
bot = TeleBot('6441187370:AAF7hTh6boSQJFeW0GeT1nhwpXYNq8Ibl1o', parse_mode='HTML')
#Мой ключ от сайта с погодой (вспомогательная переменная)
API = 'e16bc2153385f377c2f736f2bc6c50af'
#Вспомогательные переменные
currency = CurrencyConverter()
amount = 0

#Команда старт
@bot.message_handler(commands=['start'])
def cmd_start(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name},\n'
                                      f'Я телеграм бот, пошли покажу, что я могу?', reply_markup=kb.start_kb)
    bot.register_next_step_handler(message, menu)

#Главное меню
def menu(message):
    bot.send_message(message.chat.id, 'Вот, что я могу:', reply_markup=kb.menu_kb)
    bot.register_next_step_handler(message, option)

#Выбор функции
def option(message):
    string = message.text
    if string == 'Перевод слова':
        bot.send_message(message.chat.id, f'Какое слово (предложение) хотите перевести?')
        bot.register_next_step_handler(message, translate)
    elif string == 'Анекдот': #Функция анекдота
        a = generate_random_joke()

        bot.send_message(message.chat.id, a)
        bot.register_next_step_handler(message, option)
    elif string == 'Погода':
        bot.send_message(message.chat.id, f'В каком городе хотите узнать погоду?')
        bot.register_next_step_handler(message, weather)
    elif string == 'Узнать курс валют':
        bot.send_message(message.chat.id, f'Введи сумму')
        bot.register_next_step_handler(message, curr)
    elif string == 'Контакты': #Контакты
        bot.send_message(message.chat.id, 'Вот мои социальные сети:\n'
                                          'Telegram: @a4man11\n'
                                          'Instagram: https://instagram.com/mr_aiman11?igshid=MzRlODBiNWFlZA==')
        bot.register_next_step_handler(message, option)


def generate_random_joke():
    translator = Translator()

    joke = pyjokes.get_joke()
    a = translator.translate(joke, dest='ru')

    return a.text


#Оброботчики кнопок
#Функция перевода
def translate(message):
    send = translate_message(message.text)

    bot.send_message(message.chat.id, send)
    bot.send_message(message.chat.id, 'Отлично, что ещё ты хочешь узнать?')
    bot.register_next_step_handler(message, option)


def translate_message(text):
    translator = Translator()
    lang = translator.detect(text)
    lang = lang.lang

    if lang == 'ru':
        send = translator.translate(text, dest='en')
        return send.text

    else:
        send = translator.translate(text, dest='ru')
        return send.text


#Функция погоды
def weather(message):
    city = message.text.strip().lower()
    data = get_weather_by_city(city)

    if data:
        bot.send_message(message.chat.id, f'Сейчас погода в городе {message.text}: {data["main"]["temp"]} \n'
                                              f'Ощущается как: {data["main"]["feels_like"]}')
        bot.send_message(message.chat.id, 'Отлично, что ещё ты хочешь узнать?')
        bot.register_next_step_handler(message, option)
    else:
        bot.send_message(message.chat.id, f'Город не найден. Попробуйте ещё раз.')
        bot.register_next_step_handler(message, weather)


def get_weather_by_city(city):
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if not res.status_code == 200:
        return None

    return res.json()


#Функция перевода валют
def curr(message):
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Неверный формат. <b>Напишите число!</b>')
        bot.register_next_step_handler(message, curr)
        return
    if amount > 0:
        bot.send_message(message.chat.id, 'Выберете пару:', reply_markup=kb.currency_kb)
    else:
        bot.send_message(message.chat.id, 'Число должно быть <b>больше 0!</b>')
        bot.register_next_step_handler(message, curr)

#Оброботчик инлайн клавиатуры для перевода валют
@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'another':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Получается: <b>{round(res, 2)}</b>.')
        bot.send_message(call.message.chat.id, f'Отлично, что ещё ты хочешь узнать?')
        bot.register_next_step_handler(call.message, option)
    else:
        bot.send_message(call.message.chat.id, 'Введите пару значений через <b>"/"</b>, например: USD/EUR')
        bot.register_next_step_handler(call.message, anothercurrency)

#Если пользователь захотел ввести свою пару валют
def anothercurrency(message):
    try:
        values = message.text.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Получается: <b>{round(res, 2)}</b>.')
        bot.send_message(message.chat.id, f'Отлично, что ещё ты хочешь узнать?')
        bot.register_next_step_handler(message, option)
    except Exception:
        bot.send_message(message.chat.id, 'Что-то пошло не так, введите пару корректно.')
        bot.register_next_step_handler(message, anothercurrency)


if __name__ == "__main__":
    bot.polling(none_stop=True)
