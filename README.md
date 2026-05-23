<div align="center">

# 📊 Social Media Ad Performance Prediction System

### *AI-powered platform for forecasting CTR, conversions, and ROAS across major social platforms*

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2+-092E20?style=flat-square&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.4+-F7931E?style=flat-square&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Chart.js](https://img.shields.io/badge/Chart.js-4.4-FF6384?style=flat-square&logo=chart.js&logoColor=white)](https://www.chartjs.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)]()

**[Demo](#-demo) · [Features](#-features) · [Quick Start](#-quick-start) · [API](#-api-reference) · [Architecture](#-architecture)**

</div>

---

## 🎯 Overview

A production-ready ad performance forecasting platform that predicts **Click-Through Rate (CTR)**, **Conversion Rate**, and **ROAS** for marketing campaigns across **Facebook, Instagram, TikTok, LinkedIn, and X (Twitter)**.

Built with **Django** as the backend, a **Random Forest regressor** trained on 8,000+ historical campaigns, and an **interactive single-page dashboard** powered by Chart.js — the system gives marketers data-driven answers before they spend a dollar.

> *Stop guessing your ad performance. Predict it.*

---

## ✨ Features

### 🤖 Machine Learning Engine
- **Random Forest Regressor** for CTR prediction (R² ≈ 0.91)
- **Gradient Boosting Regressor** for conversion-rate forecasting (R² ≈ 0.88)
- Real-time inference via Django REST Framework
- Feature importance ranking from trained models
- 30-day day-by-day performance forecasting with ad-fatigue decay modeling

### 📊 Interactive BI Dashboard
- **Overview** — KPI cards, multi-platform CTR trends, conversion funnels, ROAS analysis
- **Audience Insights** — Age, gender, device breakdown, posting-hour heatmaps, format-platform CTR matrix
- **Platform Comparison** — Radar charts, efficiency indices, cost-per-conversion analysis
- **Forecast** — Live ML predictions with adjustable parameters and confidence scoring

### 🔌 REST API
- Clean, documented endpoints for every metric
- Prediction logging for model retraining
- CORS-enabled for cross-origin integration

### 🎨 Modern UI
- Dark theme with subtle accent palette
- Fully responsive (desktop-first)
- 20+ data visualizations powered by Chart.js
- All charts update reactively as parameters change

---
## 📈 Overview Dashboard
KPI cards · multi-platform CTR trends · conversion funnel · ROAS analysis

![Overview Dashboard](screenshots/overview.png)

## 👥 Audience Insights
Demographics · device breakdown · posting hour analysis · CTR heatmap

![Audience Insights](screenshots/audience.png)

## 🔀 Platform Comparison
5-platform radar chart · efficiency indices · cost-per-conversion analysis

![Platform Comparison](screenshots/comparison.png)

## 🤖 ML Forecasting
Real-time predictions with adjustable parameters and 30-day forecast

![ML Forecasting](screenshots/forecast.png)
---

### 📋 Feature Summary

| Tab | Visualizations |
|-----|----------------|
| **Overview** | 4 KPI cards · CTR trend · Conversions · Format ranking · Funnel · ROAS · CPC scatter |
| **Audience** | Age distribution · Devices · Gender · Industry reach · CTR heatmap · Posting hours |
| **Compare** | 5-platform radar · Efficiency vs conversion · CPC bars · Score cards |
| **Forecast** | Live predictions · vs benchmark · Feature importance · 30-day CTR/CVR forecast · Click & conversion projections |

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.10+, Django 4.2, Django REST Framework |
| **ML/AI** | Scikit-learn 1.4 (RandomForest, GradientBoosting), pandas, numpy |
| **Frontend** | Vanilla JavaScript, Chart.js 4.4, custom CSS (Inter + JetBrains Mono) |
| **Database** | SQLite (dev) — PostgreSQL-ready |
| **Dataset** | [Social Media Ad Dataset (Kaggle)](https://www.kaggle.com/datasets/ziya07/social-media-ad-dataset) |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or newer ([download](https://www.python.org/downloads/))
- Git

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/SrinivasMovva2004/Social_Media_Ad_Performace_Prediction.git
cd Social_Media_Ad_Performace_Prediction/ad_project
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Train the ML models**
```bash
python dashboard/ml/train_model.py social_media_ad_optimization.csv
```

**4. Set up the database**
```bash
python manage.py makemigrations dashboard
python manage.py migrate
```

**5. Run the Django server**
```bash
python manage.py runserver
```

**6. Open the dashboard**

Open **[http://127.0.0.1:8000](http://127.0.0.1:8000)** in your browser.

---

### One-Command Launch

For an automated setup:
```bash
python run.py
```

Open **[http://127.0.0.1:8000](http://127.0.0.1:8000)** in your browser.

---

## 📈 Model Performance

| Metric | CTR Model (RF) | CVR Model (GB) |
|--------|----------------|----------------|
| Algorithm | RandomForest (300 trees) | GradientBoosting (300 trees) |
| MAE | 0.23 | 0.84 |
| RMSE | 0.31 | 1.12 |
| R² Score | **0.912** | **0.887** |
| 5-Fold CV R² | 0.89 ± 0.02 | — |

### Top Feature Importances (CTR Model)
```
Ad Format     ████████████████████████████████  31%
Platform      ███████████████████████████       26%
Daily Budget  ██████████████████                18%
Audience Size ████████████                      12%
Duration      ████████                           8%
Industry      █████                              5%
```

---

## 🌐 API Reference

### Prediction Endpoint

```http
POST /api/predict/
Content-Type: application/json

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

**Response:**
```json
{
  "predicted_ctr":         4.21,
  "predicted_cvr":         13.8,
  "predicted_clicks":      8540,
  "predicted_conversions": 1178,
  "predicted_impressions": 201600,
  "total_spend":           7000,
  "predicted_revenue":     100130,
  "predicted_roas":        14.3,
  "confidence_score":      82.4,
  "benchmark":  { "ctr": 2.10, "cvr": 7.80, "roas": 3.1 },
  "feature_importance": [...],
  "forecast": {
    "labels": ["D1","D2",...,"D30"],
    "ctr":    [4.21, 4.18, ...],
    "cvr":    [13.8, 13.6, ...]
  }
}
```

### All Endpoints

| Method | Endpoint | Description |
|:------:|----------|-------------|
| `GET`  | `/`                        | Interactive dashboard SPA |
| `GET`  | `/api/kpis/`               | Aggregated dashboard KPIs |
| `GET`  | `/api/platform-stats/`     | Per-platform breakdown |
| `POST` | `/api/predict/`            | Run ML prediction |
| `GET`  | `/api/prediction-history/` | Last 20 predictions |
| `GET`  | `/admin/`                  | Django admin panel |

---

## 🏛 Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    BROWSER (SPA Dashboard)                   │
│         Chart.js · Vanilla JS · Reactive UI updates          │
└────────────────────────────┬─────────────────────────────────┘
                             │ HTTPS
                             ▼
┌──────────────────────────────────────────────────────────────┐
│              DJANGO REST FRAMEWORK API LAYER                 │
│      /api/predict/  ·  /api/kpis/  ·  /api/platform-stats/   │
└────────────────────────────┬─────────────────────────────────┘
                             │
              ┌──────────────┴──────────────┐
              ▼                             ▼
┌─────────────────────────┐    ┌──────────────────────────────┐
│     ML INFERENCE        │    │      DATA LAYER              │
│  RandomForest (CTR)     │    │  AdCampaign · PredictionLog  │
│  GradientBoosting (CVR) │    │  SQLite (dev) / Postgres     │
│  Joblib serialization   │    │                              │
└─────────────────────────┘    └──────────────────────────────┘
```

### Project Structure

```
ad_project/
├── 📄 manage.py                          # Django entry point
├── 📄 run.py                             # One-command launcher
├── 📄 requirements.txt                   # Python dependencies
├── 📄 social_media_ad_optimization.csv   # Training dataset
│
├── 📁 ad_performance_system/             # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── 📁 dashboard/                         # Main application
│   ├── models.py                         # AdCampaign, PredictionLog
│   ├── views.py                          # API endpoints + page views
│   ├── urls.py                           # URL routing
│   ├── admin.py                          # Django admin config
│   │
│   └── 📁 ml/                            # Machine Learning module
│       ├── train_model.py                # Train RF + GB pipelines
│       ├── predict.py                    # Inference engine
│       └── saved_models/                 # Serialized .pkl files
│
└── 📁 templates/dashboard/
    └── index.html                        # SPA dashboard (HTML+CSS+JS)
```

---

## 📚 Dataset

This project uses the **[Social Media Ad Dataset](https://www.kaggle.com/datasets/ziya07/social-media-ad-dataset)** from Kaggle, containing user engagement, ad performance, and conversion tracking data across multiple platforms.

**Features used:**
- Categorical: `platform`, `ad_format`, `objective`, `industry`
- Numerical: `daily_budget`, `audience_size`, `duration_days`

**Target variables:**
- `ctr` — Click-through rate (%)
- `conversion_rate` — Conversion rate (%)

Custom column mapping is handled in `dashboard/ml/train_model.py` (function `load_kaggle()`).

---

## 🧪 How It Works

1. **Data ingestion** — Historical campaign data loaded from CSV (Kaggle) or generated synthetically
2. **Preprocessing** — One-hot encoding for categoricals, StandardScaler for numericals
3. **Training** — Two pipelines (RF for CTR, GB for CVR) with 80/20 split + 5-fold cross-validation
4. **Serialization** — Models saved as joblib `.pkl` files for fast loading
5. **Inference** — User parameters → encoded features → model prediction → derived metrics (clicks, conversions, ROAS)
6. **Forecasting** — Base prediction propagated across 30 days with linear fatigue decay (~12% over the period)
7. **Logging** — Every prediction stored in `PredictionLog` for auditing & retraining

---

## 🛣 Roadmap

- [ ] Add real-time data ingestion via platform APIs (Meta, TikTok, LinkedIn)
- [ ] Implement A/B testing module for creative variants
- [ ] Add multi-objective optimization (budget allocation across platforms)
- [ ] Deploy demo to Railway / Render
- [ ] Add user authentication and saved campaign templates
- [ ] Export reports as PDF / PowerPoint
- [ ] Add LSTM model for time-series-aware forecasting

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| `python: command not found` | Use `python3` and `pip3` instead |
| `Permission denied` (Mac/Linux) | Add `--user` flag: `pip install --user -r requirements.txt` |
| `No module named 'django'` | Re-run `pip install -r requirements.txt` |
| Port 8000 busy | Run `python manage.py runserver 8080` |
| Models not found | Run training first: `python dashboard/ml/train_model.py` |
| `numpy build error` on Python 3.14 | Install Python 3.12 instead — many ML packages don't have 3.14 wheels yet |

---

## 📝 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Srinivas Movva**

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat-square&logo=github&logoColor=white)](https://github.com/SrinivasMovva2004)

---

## 🙏 Acknowledgments

- Dataset: [Ziya07 on Kaggle](https://www.kaggle.com/datasets/ziya07/social-media-ad-dataset)
- Charting: [Chart.js](https://www.chartjs.org/)
- Backend framework: [Django](https://www.djangoproject.com/)
- ML library: [Scikit-learn](https://scikit-learn.org/)
- Industry benchmark data: WordStream, Hootsuite ad performance reports

---

<div align="center">

**⭐ If this project helped you, please consider giving it a star!**

*Built with ❤️ using Python, Django, and Scikit-learn*

</div>