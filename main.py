
import sqlite3
import telebot
from telebot import types

TOKEN = 'YourToken'
bot = telebot.TeleBot(TOKEN)


shown_ids = []
current_person = None

def get_random_person():
    conn = sqlite3.connect('people.db')
    cursor = conn.cursor()


    if shown_ids:

        cursor.execute('SELECT id, name, photo FROM people WHERE id NOT IN ({}) ORDER BY RANDOM() LIMIT 1'.format(','.join('?' for _ in shown_ids)), shown_ids)
    else:

        cursor.execute('SELECT id, name, photo FROM people ORDER BY RANDOM() LIMIT 1')

    person = cursor.fetchone()

    conn.close()
    return person  # Возвращаем ID, имя и фото

def send_new_person(chat_id):
    global current_person  # Глобальная переменная для сохранения текущего человека

    current_person = get_random_person()  # Получаем нового случайного человека
    if current_person:
        person_id, name, photo_blob = current_person


        bot.send_photo(chat_id, photo_blob, caption="Выбери имя:")

        # Создаем кнопки с именами всех людей из базы данных
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        conn = sqlite3.connect('people.db')
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM people')
        names = cursor.fetchall()
        conn.close()

        for name_tuple in names:
            keyboard.add(types.KeyboardButton(name_tuple[0]))

        bot.send_message(chat_id, "Кто это?", reply_markup=keyboard)
    else:
        bot.send_message(chat_id, "Все фотографии уже были показаны!")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    send_new_person(message.chat.id)

@bot.message_handler(func=lambda message: True)
def check_name(message):
    global current_person

    if current_person:
        person_id, correct_name, _ = current_person

        if message.text == correct_name:
            bot.send_message(message.chat.id, "Правильно! Это " + correct_name)
            # Если правильный ответ, добавляем ID в список показанных
            shown_ids.append(person_id)
            send_new_person(message.chat.id)
        else:

            bot.send_message(message.chat.id, "Неправильно! Это был " + correct_name)


            send_new_person(message.chat.id)

    else:
        bot.send_message(message.chat.id, "Все фотографии уже были показаны!")


bot.polling()