import sqlite3

# Подключаемся к базе данных
conn = sqlite3.connect('weather_data.db')
cursor = conn.cursor()

# Проверка структуры таблицы weather
cursor.execute("PRAGMA table_info(weather);")
table_structure = cursor.fetchall()
print("Структура таблицы weather:")
for column in table_structure:
    print(column)

# Проверка данных в таблице weather
cursor.execute("SELECT * FROM weather;")
rows = cursor.fetchall()
print("\nСодержимое таблицы weather:")
if rows:
    for row in rows:
        print(row)
else:
    print("Таблица weather пуста.")

# Закрываем соединение
conn.close()
