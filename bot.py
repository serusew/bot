import telebot
import requests
from telebot import types

TOKEN = '7572351595:AAE7UUGgmiKvg1WHcHFFfOstuGFvT5ujtdg'
bot = telebot.TeleBot(TOKEN)

def get_dog_image() -> str:
    response = requests.get('https://dog.ceo/api/breeds/image/random')
    data = response.json()
    return data['message']

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Получить картинку собаки")
    item2 = types.KeyboardButton("Помощь")
    markup.add(item1, item2)

    bot.send_message(message.chat.id, 'Привет! Я WoofArt бот. Выберите действие:', reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Получить картинку собаки")
def send_dog_image(message):
    bot.send_message(message.chat.id, "Ваша картинка 🐶")
    dog_image_url = get_dog_image()
    bot.send_photo(message.chat.id, dog_image_url)

@bot.message_handler(func=lambda message: message.text == "Помощь")
def send_help(message):
    help_text = 'Этот бот отправляет случайные картинки собак. Нажмите "Получить картинку собаки", чтобы сгенерировать изображение с собакой!'
    bot.send_message(message.chat.id, help_text)

if __name__ == '__main__':
    bot.polling(none_stop=True)
