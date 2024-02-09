import telebot.types
from telebot import types

from init_bot import bot


class Questions(telebot.handler_backends.StatesGroup):
    answer_yes = telebot.handler_backends.State()
    answer_no = telebot.handler_backends.State()


@bot.message_handler(commands=['GO'])
def go(message: telebot.types.Message):
    markup = types.InlineKeyboardMarkup()
    btn_yes = types.InlineKeyboardButton('Да', callback_data='yes')
    btn_no = types.InlineKeyboardButton('Нет', callback_data='no')
    markup.add(btn_yes, btn_no)
    bot.send_message(message.chat.id, 'Тебе есть 18 лет?', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: callback.data == 'yes')
def yes(callback: telebot.types.CallbackQuery):
    bot.set_state(callback.message.from_user.id, Questions.answer_yes, callback.message.chat.id)
    bot.send_message(callback.message.chat.id, 'Высылаю список фильмов 18+:')


@bot.message_handler(state=Questions.answer_yes)
def yes(message: telebot.types.Message):
    with open('films_18+.txt', 'r', encoding='utf-8') as file:
        list_film = file.read()
    bot.send_message(message.chat.id, list_film)


@bot.callback_query_handler(func=lambda callback: callback.data == 'no')
def no(callback: telebot.types.CallbackQuery):
    bot.set_state(callback.message.from_user.id, Questions.answer_no, callback.message.chat.id)
    bot.send_message(callback.message.chat.id, 'Высылаю список фильмов до 18:')


@bot.message_handler(state=Questions.answer_no)
def yes(message: telebot.types.Message):
    with open('films_0-18.txt', 'r', encoding='utf-8') as file:
        list_film = file.read()
    bot.send_message(message.chat.id, list_film)


@bot.message_handler(state='*')
def done(message: telebot.types.Message):
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.send_message(message.chat.id, 'Приятного просмотра!')

