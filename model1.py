from sklearn.tree import DecisionTreeClassifier
import pandas as pd

# Загрузка набора данных
data = pd.read_csv('weather_data_with_recommendations.csv')

# Признаки и целевая переменная
X = data[['temp', 'humidity', 'windspeed']]
y = data['recommended_outfit']

# Обучение модели
model = DecisionTreeClassifier(random_state=42)
model.fit(X, y)
