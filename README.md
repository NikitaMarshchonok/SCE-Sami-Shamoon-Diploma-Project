# SCE‑Sami‑Shamoon‑Diploma‑Project

Weather → Wardrobe Recommender (Flask)

This app helps a user pick weather‑appropriate outfits for a selected city and date (today / next 3–4 days). Stack: Flask, OpenWeather API, simple rule‑based recommendations. A personalization ML model is planned.
--
## ✨ Key Features

  Pick location & date, fetch forecast (temp, precipitation, wind, clouds, feels‑like)

  Outfit recommendations by seasons (summer / autumn‑spring / winter / accessories) with image cards.

  Multi‑language: ru / he / en (via dictionaries; language switcher in UI).

  Request caching (TTL) to save API quota.

  Basic admin mode (protected) to upload images / edit outfit dictionaries.

  ML‑ready architecture for later personalization.

 --

## 🧠 Recommendation Logic (baseline rules)

Thresholds (editable in config.py):

Hot: tmax ≥ 28°C → tee, shorts/light pants, cap, water.

Warm: 22–27°C → tee/shirt, jeans/pants, light shoes.

Cool: 15–21°C → long‑sleeve/light jacket, jeans, closed shoes.

Cold: ≤ 14°C → sweater/hoodie + jacket, pants, warm shoes, beanie.

Precipitation: precip>0 → umbrella/raincoat, waterproof shoes.

Wind: wind_ms>7 → windbreaker/hood.

Algorithm:

From forecast derive temperature zone and flags (rain, wind, UV).

Map to seasonal sets + accessories.

Remove conflicting items, attach reasons.



## 🔮 ML Upgrade (roadmap)

Dataset: historical weather + user choices/ratings.

Features: tmin/tmax/feels, precip, wind, humidity, UV, weekday/holiday, city, user prefs.

Model: multi‑label classification (Logistic/LightGBM) or learning‑to‑rank (pairwise).

Offline metrics: F1@k / NDCG; Online: CTR/Save‑Rate, complaints↓.

A/B: Rules vs ML, tune weights.

Contact

## Author: Nikita Marshchonok
Email: n.marshchonok@gmail.com
LinkedIn: http://www.linkedin.com/in/nikita-marshchonok
GitHub: https://github.com/NikitaMarshchonok
