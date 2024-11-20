import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# Загрузка данных
data = pd.read_csv('data/weather_data_with_recommendations.csv')

# Кодирование текстового столбца 'conditions' в числовой формат
label_encoder = LabelEncoder()
data['conditions_encoded'] = label_encoder.fit_transform(data['conditions'])

# Проверка данных
print("Первые строки данных:")
print(data.head())

# Выбираем признаки и целевую переменную
X = data[['temp', 'humidity', 'windspeed', 'conditions_encoded']]
y = data['recommended_outfit']

# Обучение модели
model = DecisionTreeClassifier(criterion='gini', max_depth=5, random_state=42)
model.fit(X, y)

# Визуализация дерева решений
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt

plt.figure(figsize=(20, 10))
plot_tree(model,
          feature_names=['temp', 'humidity', 'windspeed', 'conditions_encoded'],
          class_names=model.classes_,
          filled=True)
plt.title("Дерево решений")
plt.show()
plt.savefig('decision_tree.png')

# Кросс-валидация
scores = cross_val_score(model, X, y, cv=5)  # 5-кратная кросс-валидация
print(f"Средняя точность модели на кросс-валидации: {scores.mean():.2f}")
print(f"Отклонение точности: {scores.std():.2f}")

# Кодирование всех уникальных условий
label_encoder = LabelEncoder()
label_encoder.fit(data['conditions'])

feature_importances = model.feature_importances_
for feature, importance in zip(['temp', 'humidity', 'windspeed', 'conditions_encoded'], feature_importances):
    print(f"Feature importance for {feature}: {importance:.2f}")

# Сохранение обученной модели и кодировщика
joblib.dump(model, 'outfit_recommender_model.pkl')
joblib.dump(label_encoder, 'conditions_encoder.pkl')
# Сохранение кодировщика
joblib.dump(label_encoder, 'conditions_encoder.pkl')
print("Кодировщик условий обновлён и сохранён!")
print("Модель и кодировщик успешно сохранены!")
