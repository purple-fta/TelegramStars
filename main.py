# TODO:
# [x] - Магазин подарков - добавить стикер перед выводом меню
# [x] - Топ по балансу - выделение и ник внизу 
# [x] - Ошибка - возврат звёзд
# [ ] - Пополнение звёздами
# [ ] - Авто покупка
# [ ] - Язык
# [ ] - Чеки

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

def create_giftshop_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("🎂-500🌟 [90686/500000]", callback_data="buy_gift_500"))
    keyboard.add(InlineKeyboardButton("🕯️-350🌟 [410705/500000]", callback_data="buy_gift_350"))
    keyboard.add(InlineKeyboardButton("⬅ Вернуться назад", callback_data="back_to_main_from_sticker"))
    return keyboard

def create_insufficient_balance_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("⬅ Вернуться назад", callback_data="back_to_main"))
    return keyboard

def get_top_balance_text(user_name):
    return (
        "🏆⭐ <strong>Топ по балансу звёзд.</strong> Имена скрыты в соображениях безопасности.\n\n"
        "<blockquote> 🥇 Имя скрыто 343801⭐\n"
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
        " #20 👨‍🚒 Имя скрыто 1045⭐</blockquote>\n"
        f"<blockquote><strong>#12627 👶 {user_name} 0⭐ (Вы)</strong></blockquote>"
    )

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "🎁 *Приветствую!* Я бот для автоматической покупки новых NFT подарков в телеграме\n\n"
        "Подарки от бота *можно улучшить*, но нельзя *разобрать на звёзды*.\n\n"
        "Ниже ты можешь изменить настройки под свои запросы. Дальше бот сделает всё *сам*.\n\n"
        "```\nВаш баланс: 0 ⭐```",
        parse_mode="Markdown",
        reply_markup=create_main_keyboard(),
    )


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "top_balance":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=get_top_balance_text(call.message.chat.username),
            parse_mode="HTML",
            reply_markup=create_topup_keyboard()
        )
    elif call.data == "topup":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="🌟 <b>Отправьте боту желаемое количество звёзд для пополнения. </b>\n\n"
                 "Комиссия бота 0%.",
            reply_markup=create_topup_keyboard(),
            parse_mode="HTML"
        )
    elif call.data == "giftshop":
        # Удаляем предыдущее сообщение 
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)       
        
        # Отправляем стикер c меню
        bot.send_sticker(
            chat_id=call.message.chat.id,
            sticker="CAACAgIAAxkDAAEB3wABZ-IC9x9W5qMyEVEGto1oLb_c8RAAArRbAAJhM7FL7fsQgT1iHXw2BA",
            reply_markup=create_giftshop_keyboard() # Ваша клавиатура
        )
    elif call.data == "buy_gift_500":
        balance = 0  # Пример, у пользователя 0 звёзд, нужно пополнить
        if balance < 500:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Пожалуйста, пополните счёт минимум на 500⭐, чтобы реализовать это действие.",
                reply_markup=create_insufficient_balance_keyboard()
            )
        else:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="🎂 Подарок на 500 звёзд успешно куплен!",
                reply_markup=create_giftshop_keyboard()
            )
    elif call.data == "buy_gift_350":
        balance = 0  # Пример, у пользователя 0 звёзд, нужно пополнить
        if balance < 350:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Пожалуйста, пополните счёт минимум на 350⭐, чтобы реализовать это действие.",
                reply_markup=create_insufficient_balance_keyboard()
            )
        else:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="🕯️ Подарок на 350 звёзд успешно куплен!",
                reply_markup=create_giftshop_keyboard()
            )
    elif call.data == "back_to_main":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="🎁 *Приветствую!* Я бот для автоматической покупки новых NFT подарков в телеграме\n\n"
                 "Подарки от бота *можно улучшить*, но нельзя *разобрать на звёзды*.\n\n"
                 "Ниже ты можешь изменить настройки под свои запросы. Дальше бот сделает всё *сам*.\n\n"
                 f"\nВаш баланс: 0 ⭐",
            parse_mode="Markdown",
            reply_markup=create_main_keyboard()
        )
    elif call.data == "back_to_main_from_sticker":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        send_welcome(call.message)

    elif call.data == "refund":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="💫 <strong>Мгновенный возврат звёзд.</strong>\n\n"
                 "Размер вашей транзакции должен быть у вас на балансе. "
                 "Вывод происходит в размере 100% от вашего пополнения.\n\n"
                 "<strong>Отправьте боту номер вашей транзакции вида:</strong>\n\n"
                 "stxuGTHRe_rG7ujdvx2mnRT0gdp-2yGiLkCmbhbnWhh4ZGamd3utzZukDzbpVmGMOCR107eQRjTCY8EEEtZV_EYl8lHroqo-px0G24xGJ1Ve_8\n\n"
                 "Его можно найти в вашем профиле телеграма, раздел:\n"
                 "<strong>Звёзды.</strong>",
            parse_mode="HTML",
            reply_markup=create_insufficient_balance_keyboard()
        )
    elif call.data == "purchase_history":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="*💫Вы еще не совершали покупок в нашем боте.*\n\n"
                 "*Когда вы проведете первую транзакцию, она автоматически отобразится здесь.*",
            parse_mode="Markdown",
            reply_markup=create_topup_keyboard()
        )
    elif call.data == "support_project":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="❤️ <b>Будем рады любой поддержке за нашу работу.</b>\n\n"
                 "<b>USDT TRC20</b>:" f"<blockquote>TF7MSwqV2L51sqP7F1PgCMdYhxqFCPPSQB</blockquote> \n\n"
                 "<b>TON</b>:" f"<blockquote>UQDax59lyQZrQBNdvYnJs-cpAnVNhuXX4H6PaKQlyEW33x3i</blockquote> \n\n"
                "<b>BTC</b>:" f"<blockquote> bc1q44dq3lughhtczg39q970c3thn0fxe69jlr4cgx</blockquote>",
            parse_mode="HTML",
            reply_markup=create_topup_keyboard()
        )

bot.polling()
