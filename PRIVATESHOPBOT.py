import sqlite3
import logging
import time
import telebot
from tokengit import TOKEN
from telebot import types
bot = telebot.TeleBot(TOKEN)
conn = sqlite3.connect('../base data/database.db', check_same_thread = False)
cursor = conn.cursor()
def db_table_val(user_id: int, user_name: str, user_surname: str, username: str, mesag: str,):
    cursor.execute('INSERT INTO telebotik (user_id, user_name, user_surname, username, mesag) VALUES (?, ?, ?, ?, ?)',(user_id, user_name, user_surname, username, mesag))
    conn.commit()
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width = 1)
    key1 = types.InlineKeyboardButton(text = "Месяц 🥶", callback_data = "Mes") #заложить юрл фрикассы
    key2 = types.InlineKeyboardButton(text = '3 месяца 🥵', callback_data = "Dvames") #заложить юрл фрикассы
    key3 = types.InlineKeyboardButton(text='Год подписки 🔥💥⚡️🔥🔥', callback_data = 'God')  # заложить юрл фрикассы
    markup.add(key1, key2, key3)
    #stick = open('sticker.webm', "rb")
    bot.send_animation(message.chat.id, r'https://i.gifer.com/8Vvs.gif')
    name = message.from_user.first_name
    bot.send_message(message.chat.id, f"Приветик {name}!🥰 \n Выбери кол-во дней подписки и получи доступ в нашу приватку 😈😈", reply_markup=markup, parse_mode = "html"  )
    us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username
    mes = message.text
    db_table_val(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username, mesag=mes)
@bot.callback_query_handler(func=lambda call: True)
def raschet(call):
    if call.data == "Mes":
        bot.answer_callback_query(callback_query_id=call.id, text="Вы выбрали подписку на месяц 🥰")
        knopka = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key1 = types.KeyboardButton(text = "Я оплатил")
        knopka.add(key1)
        bot.send_message(call.message.chat.id, " Перевод\n 💳💳💳 2200 2407 6828 4370\n 👤👤👤 Даниил М. \n Комментарий: Приватка\n Сумма платежа💰 100rub", reply_markup=knopka)
        bot.answer_callback_query(callback_query_id=call.id, text="Вы вы")
    if call.data == "Dvames":
        bot.answer_callback_query(callback_query_id=call.id, text="Вы выбрали подписку на 3 месяца 🥰")
        knopka = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key1 = types.KeyboardButton(text = "Я оплатил")
        knopka.add(key1)
        bot.send_message(call.message.chat.id, " Перевод\n 💳💳💳 2200 2407 6828 4370\n 👤👤👤 Даниил М. \n Комментарий: Приватка\n Сумма платежа💰 250rub", reply_markup=knopka)
    if call.data == "God":
        bot.answer_callback_query(callback_query_id=call.id, text="Вы выбрали подписку на год! 🥰")
        knopka = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key1 = types.KeyboardButton(text = "Я оплатил")
        knopka.add(key1)
        bot.send_message(call.message.chat.id, " Перевод\n 💳💳💳 2200 2407 6828 4370\n 👤👤👤 Даниил М. \n Комментарий: Приватка\n Сумма платежа💰 500rub", reply_markup=knopka)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
    bot.delete_message(call.message.chat.id, call.message.message_id)
@bot.message_handler(content_types=['text'])
def mesag(message):
    if message.text == "Я оплатил":
        message = bot.send_message(message.chat.id, "📷Отправьте скриншот оплаты📷(❌не файлом❌), ⏳ проверки займет не более 3-ex минут😌! ",reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, photo)
    else:
        bot.send_message(message.chat.id, "Не понимаю о чем ты 😪")

@bot.message_handler(content_types=['photo'])
def photo(message):
    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.file_path)
    #name = random.randrange(0, 999999)
    name2 = message.from_user.id
    with open(str(name2) + '.jpg', 'wb') as new_file:
        new_file.write(downloaded_file)
        sms = bot.send_message(message.chat.id, 'Чек принят на обработку. Ожидайте 🕜')
            #bot.send_animation(message.chat.id, r'https://i.gifer.com/3OTJR.gif', timeout = False)
            #bot.send_message("Пока твой чек обрабатывается можешь посмотреть флекс антимажи ряльна xD",)
            #bot.register_next_step_handler(sms, vid)
        vid(sms)
@bot.message_handler(content_types = ['text'])
def vid (message):
    bot.send_animation(message.chat.id, r'https://i.gifer.com/3OTJR.gif', caption =  "Пока твой чек обрабатывается можешь посмотреть флекс антимажи ряльна 😈😎😎🫡")
    #bot.send_message(message.chat.id"Пока твой чек обрабатывается можешь посмотреть флекс антимажи ряльна xD",)

while True:
    try:
        logging.info("Bot running..")
        bot.polling(none_stop=True, interval=2)

        # Предполагаю, что бот может мирно завершить работу, поэтому
        # даем выйти из цикла
        break
    except TypeError as e:
        logging.error(e)
        bot.stop_polling()

        time.sleep(15)

        logging.info("Running again!")
