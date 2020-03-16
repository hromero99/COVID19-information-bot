from telebot import TeleBot, types
import os
from dotenv import load_dotenv
from api import covid_api

load_dotenv()

bot = TeleBot(os.getenv("TELEGRAM_TOKEN"))
countries = covid_api.get_countries()
allow_countries = []
[allow_countries.extend(provinces_list) for provinces_list in countries.values() ]
print(countries)


@bot.message_handler(commands=["start"])
def say_hello(message):
    bot.reply_to(message, "Welcome to COVID19 information")


@bot.message_handler(commands=["status"])
def get_status_country(message):
    input_country = message.text.split(" ")[-1]
    if input_country in allow_countries:
        bot.reply_to(message, covid_api.get_full_status_by_country(input_country),parse_mode="Markdown")
    else:
        bot.reply_to(message, f"[!] Country {message.text.split(' ')[-1]} doesn't exist.")


bot.polling()