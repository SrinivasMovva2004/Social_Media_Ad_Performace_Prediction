# Social Media Ad Performance Prediction System

AI/ML-powered platform to **predict CTR and conversions** across Facebook, Instagram, TikTok, LinkedIn, and X/Twitter — built with Python, Django, and Scikit-learn.

---

## Dataset

**Recommended Kaggle Dataset:**
> **Social Media Ad Dataset** — User Engagement, Ad Performance, Conversion Tracking
> https://www.kaggle.com/datasets/ziya07/social-media-ad-dataset

Download the CSV and place it at the project root before training (optional — synthetic data is used by default).

---

## Quick Start (No Virtual Environment)

You only need **Python 3.10+** installed. Check with:
```bash
python --version
```

### 1. Install dependencies globally
```bash
pip install -r requirements.txt
```

If `pip` doesn't work, try `pip3`. On some systems you may need:
```bash
pip install --user -r requirements.txt
```

### 2. Train the ML models
```bash
python dashboard/ml/train_model.py
```
Trained models save to `dashboard/ml/saved_models/`.
To train on the Kaggle dataset instead:
```bash
python dashboard/ml/train_model.py path/to/social_media_ads.csv
```

### 3. Set up the database
```bash
python manage.py makemigrations dashboard
python manage.py migrate
```

### 4. Run the Django server
```bash
python manage.py runserver
```

### 5. Open the dashboard
Visit → **http://127.0.0.1:8000**

---

## Project Structure

```
ad_project/
├── manage.py
├── requirements.txt
├── README.md
│
├── ad_performance_system/          # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── dashboard/                      # Main app
│   ├── models.py                   # AdCampaign, PredictionLog
│   ├── views.py                    # Page views + REST API
│   ├── urls.py
│   ├── admin.py
│   │
│   └── ml/                         # Machine Learning module
│       ├── train_model.py          # Train RF + GB models
│       ├── predict.py              # Inference engine
│       └── saved_models/           # Serialized .pkl files
│
├── templates/dashboard/
│   └── index.html                  # Full interactive SPA dashboard
│
└── static/
    ├── css/
    └── js/
```

---

## ML Models

| Model | Algorithm | Target | Typical R² |
|---|---|---|---|
| CTR Model | RandomForestRegressor (300 trees) | Click-Through Rate (%) | ~0.91 |
| CVR Model | GradientBoostingRegressor (300 trees) | Conversion Rate (%) | ~0.88 |

**Top features by importance:**
1. Ad Format (~31%) — Video & Story outperform significantly
2. Platform (~26%) — TikTok highest raw CTR; LinkedIn highest CVR
3. Daily Budget (~18%) — Log-linear scaling effect
4. Audience Size (~12%) — Broader = lower precision
5. Duration (~8%) — Ad fatigue after ~21 days

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Dashboard SPA |
| GET | `/api/kpis/` | Aggregated dashboard KPIs |
| GET | `/api/platform-stats/` | Per-platform breakdown |
| POST | `/api/predict/` | ML prediction |
| GET | `/api/prediction-history/` | Last 20 predictions |

### Prediction request example:
```json
POST /api/predict/
{
  "platform":      "instagram",
  "ad_format":     "video",
  "objective":     "conversions",
  "industry":      "ecomm",
  "daily_budget":  500,
  "audience_size": 100000,
  "duration_days": 14
}
```

---

## Dashboard Features

- **Overview** — KPI cards, 5-platform CTR trend, ad format ranking, conversion funnel, ROAS analysis, CPC vs CVR scatter
- **Audience Insights** — Age distribution, device breakdown, gender split, posting-hour analysis (all 5 platforms), CTR heatmap (Platform × Format)
- **Platform Comparison** — Radar chart, efficiency vs conversion index, CPC comparison, overall scores
- **Forecast** — Random Forest inference, 30-day forecast with fatigue model, feature importance, cumulative conversion chart

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `python: command not found` | Use `python3` and `pip3` instead |
| `Permission denied` (Mac/Linux) | Add `--user` flag: `pip install --user -r requirements.txt` |
| `No module named 'django'` | Re-run `pip install -r requirements.txt` |
| Port 8000 busy | Run `python manage.py runserver 8080` |
| Models not found | Run training first: `python dashboard/ml/train_model.py` |
| `ModuleNotFoundError: sklearn` | Run `pip install scikit-learn==1.4.0` directly |
