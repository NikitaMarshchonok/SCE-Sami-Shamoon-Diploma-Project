import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib

# Пример данных для обучения
data = {
    'temp': [15, 25, 5, -2, 30],
    'humidity': [60, 80, 75, 40, 20],
    'windspeed': [5, 3, 10, 2, 6],
    'weather_code': [800, 801, 600, 602, 802],  # Пример кодов погоды
    'outfit': ['t-shirt', 'light jacket', 'winter coat', 'heavy coat', 'shorts']
}

df = pd.DataFrame(data)

# Целевая переменная и признаки
X = df[['temp', 'humidity', 'windspeed', 'weather_code']]
y = df['outfit']

# Обучение модели
model = DecisionTreeClassifier(random_state=42)
model.fit(X, y)

# Сохранение модели
joblib.dump(model, 'outfit_recommender_model.pkl')
print("Модель успешно сохранена с новыми признаками!")
