import telebot
import json
import random
import os
from dotenv import load_dotenv

load_dotenv()
BOT_API = os.getenv('BOT_API')

tasks_info = open('/data/output.json', 'r', encoding='utf-8')
tasks = open('/data/tasks.json', 'r', encoding='utf-8')
try:
    data = json.load(tasks_info)
    tasks_data = json.load(tasks)
finally:
    tasks_info.close()
    tasks.close()

tasks_button = data.keys()
example_buttons = tasks_data.keys()

bot = telebot.TeleBot(BOT_API)

@bot.message_handler(commands=["start"])
def main(message):
    bot.send_message(message.chat.id, "Этот бот создан для помощи школьникам в подгтовке к ЕГЭ")

@bot.message_handler(commands=["info"])
def main(message):
    bot.send_message(message.chat.id, "Основные команды: \n"
                                      "1. /start - запуск бота \n"
                                      "2. /menu - отображение меню \n"
                                      "3. /help - связаться с админом")

@bot.message_handler(commands=["menu"])
def main(message):
    menu = telebot.types.InlineKeyboardMarkup()
    get_info = telebot.types.InlineKeyboardButton("получить информацию по "
                                                  "заданию",
                                                  callback_data="info")
    get_tasks = telebot.types.InlineKeyboardButton("получить задания",
                                                   callback_data="tasks")

    menu.row(get_info)
    menu.row(get_tasks)
    bot.send_message(message.chat.id, "Выберите нужный раздел",
                     reply_markup=menu)

@bot.callback_query_handler(func=lambda callback: True)
def main(callback):
    id = callback.message.chat.id

    if callback.data == "info":
        send_info(id)
    elif callback.data == "tasks":
        send_task(id)

    if callback.data in tasks_button:
        bot.send_message(id, data[callback.data])

def send_info(id):
    task_menu = telebot.types.InlineKeyboardMarkup()

    for button in tasks_button:
       new_button = telebot.types.InlineKeyboardButton(button,
                                                   callback_data=button)
       task_menu.row(new_button)

    bot.send_message(id, "Список заданий", reply_markup=task_menu)

def send_task(id):
    task_menu = telebot.types.InlineKeyboardMarkup()

    for button in example_buttons:
        new_button = telebot.types.InlineKeyboardButton(
            button, url=random.choice(tasks_data[button]))
        task_menu.row(new_button)

    bot.send_message(id, "Выберите задачу", reply_markup=task_menu)



@bot.message_handler()
def main(message):
    if message.text.lower() == "привет":
        bot.send_message(message.chat.id, "Привет😁")
    elif message.text.lower() == "пока":
        bot.send_message(message.chat.id, "Я буду скучать😪")
    elif message.text.lower() == "как дела?":
        bot.send_message(message.chat.id, "Круто, спасибо,что спросили😋")
    else:
        bot.send_message(message.chat.id, "Моя твоя не понимать😓")

bot.polling()