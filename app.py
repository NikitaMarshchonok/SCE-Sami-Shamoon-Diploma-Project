from flask import Flask, render_template, request, flash
import requests
import joblib
import pandas as pd
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import sqlite3



app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Load the trained model
#model = joblib.load('outfit_recommender_model.pkl')
# Загрузка модели и энкодеров
model = joblib.load('outfit_recommender_model.pkl')
conditions_encoder = joblib.load('conditions_encoder.pkl')
#outfit_encoder = joblib.load('outfit_encoder.pkl')

# Function to format outfit recommendations
def format_recommendation(outfit):
    recommendations = {
        "t-shirt": "Сегодня тепло, футболка будет отличным выбором для комфортного дня.",
        "light jacket": "Погода прохладная. Легкая куртка идеально подойдет, чтобы чувствовать себя комфортно.",
        "winter coat": "Рекомендуется надеть зимнее пальто, чтобы оставаться в тепле в холодную погоду.",
        "heavy coat": "Очень холодно! Очень теплое пальто поможет вам согреться в такую погоду.",
        "shorts": "Очень жарко! Шорты подойдут лучше всего, чтобы чувствовать себя комфортно."
    }
    return recommendations.get(outfit, f"Рекомендуем: {outfit}.")


# Fetch weather forecast data
def get_weather_forecast(city):
    api_key = '6aa6124072c365072c213b7bb0269b45'
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric&lang=ru'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def save_weather_to_db(city, forecast_data):
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()

    for item in forecast_data['list']:
        date = item['dt_txt'].split(' ')[0]
        temperature = item['main']['temp']
        humidity = item['main']['humidity']
        wind_speed = item['wind']['speed']

        # Проверка на дубликаты, чтобы не записывать те же данные несколько раз
        cursor.execute("""
            SELECT * FROM weather WHERE city = ? AND date = ?
        """, (city, date))
        result = cursor.fetchone()

        if not result:
            # Вставка данных, если записи еще нет
            cursor.execute("""
                INSERT INTO weather (city, date, temperature, humidity, wind_speed)
                VALUES (?, ?, ?, ?, ?)
            """, (city, date, temperature, humidity, wind_speed))
            print(f"Inserting data: {city}, {date}, {temperature}, {humidity}, {wind_speed}")

    conn.commit()
    conn.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error_message = None
    forecast_dates = []
    forecast_temps = []
    forecast_humidity = []
    forecast_wind_speed = []
    formatted_outfit_recommendation = None
    selected_date = request.form.get('date', datetime.now().strftime('%Y-%m-%d'))

    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            forecast_data = get_weather_forecast(city)
            if forecast_data:
                save_weather_to_db(city, forecast_data)
                # Process forecast data for the selected date
                for item in forecast_data['list']:
                    date = item['dt_txt'].split(' ')[0]
                    if date == selected_date:
                        temperature = item['main']['temp']
                        humidity = item['main']['humidity']
                        wind_speed = item['wind']['speed']
                        conditions = item['weather'][0]['description']

                        # Обработка неизвестных условий
                        try:
                            conditions_encoded = conditions_encoder.transform([conditions])[0]
                        except ValueError:
                            error_message = f"Условие '{conditions}' не распознано. Используется значение по умолчанию."
                            print(error_message)
                            conditions_encoded = 0  # Значение по умолчанию

                        # Prepare data for the model
                        input_data = pd.DataFrame([[temperature, humidity, wind_speed, conditions_encoded]],
                                                  columns=['temp', 'humidity', 'windspeed', 'conditions_encoded'])

                        # Predict outfit
                        try:
                            outfit_recommendation = model.predict(input_data)[0]
                            formatted_outfit_recommendation = format_recommendation(outfit_recommendation)
                            weather_data = {
                                'name': city,
                                'main': {'temp': temperature, 'humidity': humidity},
                                'wind': {'speed': wind_speed},
                                'weather': [{'description': item['weather'][0]['description']}]
                            }
                        except Exception as e:
                            error_message = f"Ошибка при предсказании: {e}"
                        break
                # Prepare data for the chart (for the next 5 days)
                for item in forecast_data['list']:
                    forecast_date = item['dt_txt'].split(' ')[0]
                    if forecast_date not in forecast_dates:
                        forecast_dates.append(forecast_date)
                        forecast_temps.append(item['main']['temp'])
                        forecast_humidity.append(item['main']['humidity'])
                        forecast_wind_speed.append(item['wind']['speed'])
            else:
                error_message = "Не удалось найти город. Попробуйте снова."

    return render_template('index.html', weather=weather_data, outfit=formatted_outfit_recommendation,

                           forecast_dates=forecast_dates, forecast_temps=forecast_temps,
                           forecast_humidity=forecast_humidity, forecast_wind_speed=forecast_wind_speed,
                           selected_date=selected_date, min_date=datetime.now().strftime('%Y-%m-%d'),
                           max_date=(datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d'))




# ETL код
def init_db():
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS weather (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       city TEXT,
                       date TEXT,
                       temperature REAL,
                       humidity REAL,
                       wind_speed REAL
                   )''')
    conn.commit()
    conn.close()


def weather_etl():
    city = "Netanya"
    forecast_data = get_weather_forecast(city)

    if forecast_data:
        conn = sqlite3.connect('weather_data.db')
        cursor = conn.cursor()

        for item in forecast_data['list']:
            date = item['dt_txt'].split(' ')[0]
            temperature = item['main']['temp']
            humidity = item['main']['humidity']
            wind_speed = item['wind']['speed']

            # Отладочный вывод
            print(f"Inserting data: {city}, {date}, {temperature}, {humidity}, {wind_speed}")

            cursor.execute("""
                INSERT INTO weather (city, date, temperature, humidity, wind_speed)
                VALUES (?, ?, ?, ?, ?)
            """, (city, date, temperature, humidity, wind_speed))

        conn.commit()
        conn.close()
    else:
        print("No data received from API")


scheduler = BackgroundScheduler()
scheduler.add_job(weather_etl, 'interval', minutes=55)
scheduler.start()

init_db()


if __name__ == '__main__':
    app.run(debug=True)
