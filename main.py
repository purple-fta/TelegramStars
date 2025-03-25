import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
import os
from loguru import logger
import sys

load_dotenv()
API_TOKEN = os.getenv('TELEGRAM_API_KEY')


bot = telebot.TeleBot(API_TOKEN)

users = {}


# Функция, которая будет обрабатывать команду /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🎁 Приветствую! Я бот для автоматической покупки новых NFT подарков в телеграме\n\nПодарки от бота можно улучшить, но нельзя разобрать на звёзды.\n\nНиже ты можешь изменить настройки под свои запросы. Дальше бот сделает всё сам.\n\n" +  f"```\nВаш баланс: 0 ⭐```", parse_mode="MARKDOWN" )


# # Запуск бота
bot.polling()