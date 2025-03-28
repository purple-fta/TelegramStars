import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
import os

load_dotenv()
API_TOKEN = os.getenv('TELEGRAM_API_KEY')

bot = telebot.TeleBot(API_TOKEN)

users_states = {}

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

def get_top_balance_text(user_name, user_id):
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
        f"<blockquote><strong>#12627 👶 {user_name} {users_states[user_id]["coins"]}⭐ (Вы)</strong></blockquote>"
    )

def create_autobuy_keyboard(user_id):
    keyboard = InlineKeyboardMarkup(row_width=2)
    text = "🟢 Включён" if users_states[user_id]["on"] else "🔴 Выключен"
    keyboard.add(InlineKeyboardButton(text, callback_data="enable"))
    keyboard.add(
        InlineKeyboardButton(f"От: {users_states[user_id]["min"]} ⭐", callback_data="min"),
        InlineKeyboardButton(f"До: {users_states[user_id]["max"]} ⭐", callback_data="max")
    )
    keyboard.add(InlineKeyboardButton(f"Саплай: {users_states[user_id]["spline"]} 🎁", callback_data="spline"))
    keyboard.add(InlineKeyboardButton("⬅ Вернуться назад", callback_data="back_to_main"))

    return keyboard

def create_buy_gift_keyboard(cost, amount):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(f"Купить за {cost} 🌟", callback_data=f"buy_gift_{cost}_really"))
    keyboard.add(InlineKeyboardButton(f"{amount} из 500000 🎁", callback_data=f"sdfgvsdv"))
    keyboard.add(InlineKeyboardButton(f"Улучшить за 25 🌟", callback_data=f"sdfg"))
    keyboard.add(InlineKeyboardButton(f"⬅ Вернуться назад", callback_data=f"back_to_giftshop"))

    return keyboard


def process_enter(message, opt):
    if message.from_user.id in users_states:
        if message.text.isdigit():
            if opt == "donate":
                bot.send_invoice(
                    chat_id=message.chat.id,
                    title="Пополнение счёта",
                    description=f"Оплата {int(message.text)} звёзд.",
                    invoice_payload="Пополнение счёта",
                    currency="XTR",
                    prices=[telebot.types.LabeledPrice("XTR", int(message.text))],
                    provider_token=""   
                )
            else:
                users_states[message.from_user.id][opt] = int(message.text)
                send_autobuy(message)
        

@bot.pre_checkout_query_handler(func=lambda query: True)
def pre_checkout_query(pre_checkout_query):
    """
    Обработчик pre-checkout запроса. Подтверждает возможность оплаты.
    """
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.from_user.id not in users_states:
        users_states[message.from_user.id] = {"min": 0, "max": 0, "spline": 0, "on": False, "coins": 0, "upgrade": False, "amount": 0, "cost": 0}
        
    bot.send_message(
        message.chat.id,
        "🎁 *Приветствую!* Я бот для автоматической покупки новых NFT подарков в телеграме\n\n"
        "Подарки от бота *можно улучшить*, но нельзя *разобрать на звёзды*.\n\n"
        "Ниже ты можешь изменить настройки под свои запросы. Дальше бот сделает всё *сам*.\n\n"
        f"```\nВаш баланс: {users_states[message.from_user.id]["coins"]} ⭐```",
        parse_mode="Markdown",
        reply_markup=create_main_keyboard(),
    )

def get_amount(message, cost, old_message_id):
    if message.text.isdigit():
        bot.delete_message(chat_id=message.chat.id, message_id=old_message_id)
        users_states[message.from_user.id]["amount"] = int(message.text)
        users_states[message.from_user.id]["cost"] = cost
        bot.send_message(
            chat_id=message.chat.id,
            text=f"❗️ <b>Вы уверены что хотите купить </b> {message.text} 🎁 за {cost*int(message.text)} 🌟",
            reply_markup=InlineKeyboardMarkup(row_width=1).add(
                InlineKeyboardButton("🌟 Купить", callback_data="buy"),
                InlineKeyboardButton(("✅" if users_states[message.from_user.id]["upgrade"] else "❌") + "Улучшение (+25🌟 каждый)", callback_data="upgrade_switch"),
                InlineKeyboardButton("⬅ Вернуться назад", callback_data="giftshop"),
            ),
            parse_mode="HTML"
        )  

def send_autobuy(call):
    bot.send_message(
        chat_id=call.chat.id,
        text="🤖 <b>Меню автоматической покупки.</b>\n\n"
                "<i>Приоритет в автопокупке имеют люди с самым большим балансом. Бот покупает самый лимитированный подарок из вышедших, учитывая ваши настройки.</i>\n\n"
                "🎁 <b>Саплай:</b> количество копий вышедшего подарка. Если саплай подарка превышает ваши настройки, автобай не будет его покупать.",
        parse_mode="HTML",
        reply_markup=create_autobuy_keyboard(call.from_user.id)
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "top_balance":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=get_top_balance_text(call.message.chat.username, call.from_user.id),
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

        bot.register_next_step_handler(call.message, process_enter, "donate")
    elif call.data == "giftshop":
        users_states[call.from_user.id]["upgrade"] = False

        # Удаляем предыдущее сообщение 
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)       
        
        # Отправляем стикер c меню
        bot.send_sticker(
            chat_id=call.message.chat.id,
            sticker="CAACAgIAAxkDAAEB3wABZ-IC9x9W5qMyEVEGto1oLb_c8RAAArRbAAJhM7FL7fsQgT1iHXw2BA",
            reply_markup=create_giftshop_keyboard() # Ваша клавиатура
        )
    elif call.data == "buy_gift_500":
        # bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)  
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=create_buy_gift_keyboard(500, "67 497") # Ваша клавиатура
        )
    elif call.data == "buy_gift_350":
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=create_buy_gift_keyboard(350, "408 163") # Ваша клавиатура
        )
    elif call.data == "buy_gift_350_really":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        old_message_id = bot.send_message(
            call.message.chat.id,
            text="🎁 Отправьте боту желаемое количество подарков для покупки:",
            reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("⬅ Вернуться назад", callback_data="back_buy_gift_350"))
        ).id
        bot.register_next_step_handler(call.message, get_amount, 350, old_message_id)
    elif call.data == "buy_gift_500_really":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        old_message_id = bot.send_message(
            call.message.chat.id,
            text="🎁 Отправьте боту желаемое количество подарков для покупки:",
            reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("⬅ Вернуться назад", callback_data="back_buy_gift_500"))
        ).id
        bot.register_next_step_handler(call.message, get_amount, 500, old_message_id)
    elif call.data == "back_buy_gift_500":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_sticker(
            chat_id=call.message.chat.id,
            sticker="CAACAgIAAxkDAAEB3wABZ-IC9x9W5qMyEVEGto1oLb_c8RAAArRbAAJhM7FL7fsQgT1iHXw2BA",
            reply_markup=create_buy_gift_keyboard(500, "67 497") # Ваша клавиатура
        )
    elif call.data == "back_buy_gift_350":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_sticker(
            chat_id=call.message.chat.id,
            sticker="CAACAgIAAxkDAAEB3wABZ-IC9x9W5qMyEVEGto1oLb_c8RAAArRbAAJhM7FL7fsQgT1iHXw2BA",
            reply_markup=create_buy_gift_keyboard(350, "408 163") # Ваша клавиатура
        )
    elif call.data == "back_to_giftshop":
        bot.edit_message_reply_markup(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=create_giftshop_keyboard() # Ваша клавиатура
        )
    elif call.data == "back_to_main":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="🎁 *Приветствую!* Я бот для автоматической покупки новых NFT подарков в телеграме\n\n"
            "Подарки от бота *можно улучшить*, но нельзя *разобрать на звёзды*.\n\n"
            "Ниже ты можешь изменить настройки под свои запросы. Дальше бот сделает всё *сам*.\n\n"
            f"```\nВаш баланс: {users_states[call.from_user.id]["coins"]} ⭐```",
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
                 "<blockquote>stxuGTHRe_rG7ujdvx2mnRT0gdp-2yGiLkCmbhbnWhh4ZGamd3utzZukDzbpVmGMOCR107eQRjTCY8EEEtZV_EYl8lHroqo-px0G24xGJ1Ve_8</blockquote>\n\n"
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
    elif call.data == "change_language":
        bot.answer_callback_query(call.id, "😴 Coming soon...")
    elif call.data == "checks":
        bot.answer_callback_query(call.id, "😴 Эта функция ещё в разработке")
    elif call.data == "autobuy":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="🤖 <b>Меню автоматической покупки.</b>\n\n"
                 "<i>Приоритет в автопокупке имеют люди с самым большим балансом. Бот покупает самый лимитированный подарок из вышедших, учитывая ваши настройки.</i>\n\n"
                 "🎁 <b>Саплай:</b> количество копий вышедшего подарка. Если саплай подарка превышает ваши настройки, автобай не будет его покупать.",
            parse_mode="HTML",
            reply_markup=create_autobuy_keyboard(call.from_user.id)
        )
    elif call.data == "enable":
        users_states[call.from_user.id]["on"] =  not users_states[call.from_user.id]["on"]
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="🤖 <b>Меню автоматической покупки.</b>\n\n"
                 "<i>Приоритет в автопокупке имеют люди с самым большим балансом. Бот покупает самый лимитированный подарок из вышедших, учитывая ваши настройки.</i>\n\n"
                 "🎁 <b>Саплай:</b> количество копий вышедшего подарка. Если саплай подарка превышает ваши настройки, автобай не будет его покупать.",
            parse_mode="HTML",
            reply_markup=create_autobuy_keyboard(call.from_user.id)
        )
    elif call.data == "min":
        bot.edit_message_text("⭐️ Отправьте боту <b>минимальную</b> цену подарка для покупки:", call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("⬅ Вернуться назад", callback_data="back_to_autobuy")))
        bot.register_next_step_handler(call.message, process_enter, "min")
    elif call.data == "back_to_autobuy":
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="🤖 <b>Меню автоматической покупки.</b>\n\n"
                 "<i>Приоритет в автопокупке имеют люди с самым большим балансом. Бот покупает самый лимитированный подарок из вышедших, учитывая ваши настройки.</i>\n\n"
                 "🎁 <b>Саплай:</b> количество копий вышедшего подарка. Если саплай подарка превышает ваши настройки, автобай не будет его покупать.",
            parse_mode="HTML",
            reply_markup=create_autobuy_keyboard(call.from_user.id)
        )
    elif call.data == "max":
        bot.edit_message_text("⭐️ Отправьте боту <b>максимальную</b> цену подарка для покупки:", call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("⬅ Вернуться назад", callback_data="back_to_autobuy")))
        bot.register_next_step_handler(call.message, process_enter, "max")
    elif call.data == "spline":
        bot.edit_message_text("🎁 Отправьте боту лимит количества подарков (саплай):", call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("⬅ Вернуться назад", callback_data="back_to_autobuy")))
        bot.register_next_step_handler(call.message, process_enter, "spline")
    elif call.data == "upgrade_switch":
        users_states[call.from_user.id]["upgrade"] = not users_states[call.from_user.id]["upgrade"]
        if users_states[call.from_user.id]["upgrade"]:
            users_states[call.from_user.id]["cost"]+=25
        else:
            users_states[call.from_user.id]["cost"]-=25

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            text=f"❗️ <b>Вы уверены что хотите купить </b> {users_states[call.from_user.id]["amount"]} 🎁 за {users_states[call.from_user.id]["cost"]*int(users_states[call.from_user.id]["amount"])} 🌟",
            reply_markup=InlineKeyboardMarkup(row_width=1).add(
                InlineKeyboardButton("🌟 Купить", callback_data="buy"),
                InlineKeyboardButton(("✅" if users_states[call.from_user.id]["upgrade"] else "❌") + "Улучшение (+25🌟 каждый)", callback_data="upgrade_switch"),
                InlineKeyboardButton("⬅ Вернуться назад", callback_data="giftshop"),
            ),
            parse_mode="HTML"
        )
    elif call.data == "buy":
        if users_states[call.from_user.id]["coins"] < users_states[call.from_user.id]["amount"]*users_states[call.from_user.id]["cost"]:
            bot.edit_message_text(
                text=f"У вас не хватает {users_states[call.from_user.id]["amount"]*users_states[call.from_user.id]["cost"]-users_states[call.from_user.id]["coins"]} 🌟",
                chat_id=call.message.chat.id,
                message_id=call.message.id,
                reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton("💳 Пополнить счёт", callback_data="topup")
                )
            )


@bot.message_handler(content_types=['successful_payment'])
def successful_payment(message):
    """
    Обработчик успешного платежа.
    """
    users_states[message.from_user.id]["coins"] += 1
    send_welcome(message)



bot.polling()
