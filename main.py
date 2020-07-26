import telebot
import websocket
from googletrans import Translator
import requests

translator = Translator()
r = requests.get(
    'https://finnhub.io/api/v1/news?category=general&token=bsdu2h7rh5rea8ra92n0')
res = r.json()

bot = telebot.TeleBot('1397668950:AAHXnmLwu5e8rFgMOVME8pDRHhuADkEveic')

stickers_keyboard = telebot.types.ReplyKeyboardMarkup()
stickers_keyboard.row('Собака', "Кошка", "Последние новости", "Команды")

stickerMessagesObject = {
    "собака": 'CAACAgIAAxkBAAMaXxvckKnvA2ESVw2gm8mUZLAQkOMAApkIAAJcAmUDA9621i3T6g4aBA',
    'кошка': 'CAACAgIAAxkBAAMPXxva-i4yfYcv21CHH-SaZiMk9UwAAsoEAAIcktIDPxEeanJ4Hu4aBA'
}

newsMessagesObject = {
    "последние новости": res[0]
}

commandsMessagesObject = {
    "команды": """
        собака - показать собаку,
        кошка - показать кошку,
        последние новости - показать последние новости,
        новости [1-20] - показать новость под номером [1-20]
        новости [от какой] [кол-во] - показать от [от какой] новости [кол-во] новостей
    """
}


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, '{0}, i got your message. Thanks for it.'.format(
        message.from_user.first_name), reply_markup=stickers_keyboard)


@bot.message_handler(content_types=['sticker'])
def get_sticker(message):
    print(message)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() in stickerMessagesObject:
        bot.send_sticker(
            message.chat.id, stickerMessagesObject[message.text.lower()])

    elif message.text.lower() in newsMessagesObject:
        bot.send_message(message.chat.id, translator.translate(
            newsMessagesObject[message.text.lower()]["headline"], dest='ru').text)
        bot.send_message(
            message.chat.id, (newsMessagesObject[message.text.lower()]["url"]))

    elif message.text.lower() in commandsMessagesObject:
        bot.send_message(
            message.chat.id, commandsMessagesObject[message.text.lower()])

    elif message.text.lower() in commandsMessagesObject:
        bot.send_message(
            message.chat.id, commandsMessagesObject[message.text.lower()])

    elif "новости" in message.text.lower() and message.text.lower() != "последние новости" and len(message.text.lower().split(" ")) == 2:
        try:
            bot.send_message(message.chat.id, translator.translate(
                res[int(message.text.split(" ")[1])]["headline"], dest='ru').text)
            bot.send_message(
                message.chat.id, (res[int(message.text.split(" ")[1])]["url"]))
        except IndexError:
            bot.send_message(
                message.chat.id, "Извините но с таким ID новости нет")

    elif "новости" in message.text.lower() and message.text.lower() != "последние новости" and len(message.text.lower().split(" ")) == 3:
        try:
            fromNumber = int(message.text.split(" ")[1])
            toNumber = int(message.text.split(" ")[2])
            for i in range(fromNumber, toNumber+1):
                bot.send_message(message.chat.id, translator.translate(
                    res[i]["headline"], dest='ru').text)
                bot.send_message(
                    message.chat.id, (res[i]["url"]))
        except IndexError:
            bot.send_message(
                message.chat.id, "Извините но с таким ID новости нет")


bot.polling()
