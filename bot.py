import telebot
import json
import credentials
import requests

r = requests.get('http://localhost:5000/friends')

bot = telebot.TeleBot(credentials.BOT_TOKEN)

parsed_json = json.loads(r.content)


@bot.message_handler(commands=['friends'])
def start_message(message):
    bot.send_message(message.chat.id, json.dumps(parsed_json, indent=4, sort_keys=True))


bot.polling()
