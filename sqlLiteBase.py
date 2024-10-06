import sqlite3

# Подключаемся к базе данных
conn = sqlite3.connect('people.db')
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS people (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    photo BLOB NOT NULL
)
''')

# Функция для добавления людей в базу данных
def add_person(name, file_path):
    with open(file_path, 'rb') as file:  #
        blob = file.read()
    cursor.execute('''
        INSERT INTO people (name, photo)
        VALUES (?, ?)
    ''', (name, blob))
    conn.commit()


# add_person('Kratos', 'D:/hobie/telegramBotSQlite/kratos.jpg')
# add_person('Napoleon', 'D:/hobie/telegramBotSQlite/napoleon.jpg')
# add_person('George Smit Patton', 'D:/hobie/telegramBotSQlite/General_George_S_Patton.jpg')
# add_person('Bernard_Montgomery', 'D:/hobie/telegramBotSQlite/General_Sir_Bernard_Montgomery_in_England,_1943_TR1037.jpg')
# add_person('Heinz Wilhelm Guderian', 'D:/hobie/telegramBotSQlite/Heinz_Guderian_portrait.jpg')
# Закрываем соединение
conn.close()
