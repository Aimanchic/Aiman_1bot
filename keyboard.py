from telebot import types #импорт чтоб работали клавиатуры

#Начало
start_kb = types.ReplyKeyboardMarkup(row_width=1)
start_kb_but1 = types.KeyboardButton(text='Пошли!')
start_kb.add(start_kb_but1)

#Клавиатура меню
menu_kb = types.ReplyKeyboardMarkup(row_width=2)
menu_kb_but1 = types.KeyboardButton(text='Перевод слова')
menu_kb_but2 = types.KeyboardButton(text='Узнать курс валют')
menu_kb_but3 = types.KeyboardButton(text='Погода')
menu_kb_but4 = types.KeyboardButton(text='Анекдот')
menu_kb_but5 = types.KeyboardButton(text='Контакты')
menu_kb.add(menu_kb_but1, menu_kb_but2, menu_kb_but3, menu_kb_but4, menu_kb_but5)

#Клавиатура перевода валют
currency_kb = types.InlineKeyboardMarkup(row_width=2)
currency_kb_but1 = types.InlineKeyboardButton('RUB/USD', callback_data='RUB/USD')
currency_kb_but2 = types.InlineKeyboardButton('RUB/EUR', callback_data='RUB/EUR')
currency_kb_but3 = types.InlineKeyboardButton('USD/EUR', callback_data='USD/EUR')
currency_kb_but4 = types.InlineKeyboardButton('Другое', callback_data='another')
currency_kb.add(currency_kb_but1, currency_kb_but2, currency_kb_but3, currency_kb_but4)

