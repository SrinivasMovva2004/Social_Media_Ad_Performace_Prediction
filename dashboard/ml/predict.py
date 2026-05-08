"""
predict.py
==========
Loads trained Scikit-learn pipelines and returns performance predictions.
All predictions go through real RandomForest / GradientBoosting models.
"""

import math
import joblib
import numpy as np
import pandas as pd
from pathlib import Path

MODEL_DIR = Path(__file__).parent / 'saved_models'

# Singletons — loaded once per process
_ctr_model = None
_cvr_model = None
_feat_imp  = None


def _load():
    global _ctr_model, _cvr_model, _feat_imp
    if _ctr_model is not None:
        return
    ctr_path = MODEL_DIR / 'ctr_model.pkl'
    cvr_path = MODEL_DIR / 'cvr_model.pkl'
    if not ctr_path.exists():
        raise FileNotFoundError(
            'Trained models not found.\n'
            'Run:  python dashboard/ml/train_model.py\n'
            'to generate them first.'
        )
    _ctr_model = joblib.load(ctr_path)
    _cvr_model = joblib.load(cvr_path)
    imp_path   = MODEL_DIR / 'feature_importance.pkl'
    _feat_imp  = joblib.load(imp_path) if imp_path.exists() else {}


# Average order value by industry (used for ROAS estimation)
AOV_MAP = {'ecomm': 85, 'saas': 240, 'fin': 320, 'health': 65, 'edu': 150}

# Industry benchmarks (CTR %, CVR %, ROAS)
BENCHMARKS = {
    'facebook':  {'ctr': 2.50, 'cvr': 9.21,  'roas': 3.5},
    'instagram': {'ctr': 2.10, 'cvr': 7.80,  'roas': 3.1},
    'tiktok':    {'ctr': 3.00, 'cvr': 5.50,  'roas': 2.8},
    'linkedin':  {'ctr': 0.78, 'cvr': 12.00, 'roas': 4.2},
    'twitter':   {'ctr': 0.86, 'cvr': 4.10,  'roas': 2.2},
}


def _confidence(budget, audience_size, duration_days):
    """
    Heuristic confidence score (50–97%).
    Larger budget + bigger audience + longer duration → higher confidence.
    """
    s  = 50.0
    s += min(16.0, math.log10(max(budget, 50)) * 5)
    s += min(10.0, math.log10(max(audience_size, 1e4) / 1e4) * 3)
    s += min(12.0, duration_days * 0.35)
    return round(min(97.0, s), 1)


def predict(
    platform: str,
    ad_format: str,
    objective: str,
    industry: str,
    daily_budget: float,
    audience_size: int,
    duration_days: int,
) -> dict:
    """
    Run both ML models and return full prediction payload.

    Returns
    -------
    dict with keys:
        predicted_ctr, predicted_cvr, predicted_clicks,
        predicted_conversions, predicted_impressions,
        total_spend, predicted_revenue, predicted_roas,
        confidence_score, benchmark, feature_importance, forecast
    """
    _load()

    X = pd.DataFrame([{
        'platform':     platform,
        'ad_format':    ad_format,
        'objective':    objective,
        'industry':     industry,
        'daily_budget': daily_budget,
        'audience_size': audience_size,
        'duration_days': duration_days,
    }])

    ctr = max(0.1, float(_ctr_model.predict(X)[0]))
    cvr = max(0.5, float(_cvr_model.predict(X)[0]))

    impressions = int(audience_size * 0.12 * duration_days)
    clicks      = int(impressions * (ctr / 100))
    conversions = int(clicks * (cvr / 100))
    spend       = round(daily_budget * duration_days, 2)
    revenue     = conversions * AOV_MAP.get(industry, 100)
    roas        = round(revenue / spend, 2) if spend > 0 else 0.0
    conf        = _confidence(daily_budget, audience_size, duration_days)

    bench = BENCHMARKS.get(platform, BENCHMARKS['facebook']).copy()

    feat_list = [
        {'feature': k, 'importance': round(v * 100, 1), 'importance_raw': v}
        for k, v in sorted(_feat_imp.items(), key=lambda x: -x[1])
    ]

    return {
        'predicted_ctr':          round(ctr, 3),
        'predicted_cvr':          round(cvr, 3),
        'predicted_clicks':       clicks,
        'predicted_conversions':  conversions,
        'predicted_impressions':  impressions,
        'total_spend':            spend,
        'predicted_revenue':      revenue,
        'predicted_roas':         roas,
        'confidence_score':       conf,
        'benchmark':              bench,
        'feature_importance':     feat_list,
        'forecast':               _forecast(ctr, cvr, audience_size, duration_days),
    }


def _forecast(base_ctr, base_cvr, audience_size, duration_days, days=30):
    """Generate a 30-day forecast with ad-fatigue decay + deterministic noise."""
    rng = np.random.default_rng(42)
    daily_imp = audience_size * 0.12
    labels, ctr_fc, cvr_fc, click_fc, conv_fc = [], [], [], [], []
    cum_conv = 0

    for d in range(days):
        fatigue   = 1 - (d / days) * 0.12
        noise_ctr = rng.normal(0, 0.06)
        noise_cvr = rng.normal(0, 0.04)
        c_ctr = max(0.1, round(base_ctr * fatigue + noise_ctr, 3))
        c_cvr = max(0.2, round(base_cvr * fatigue + noise_cvr, 3))
        d_clicks = int(daily_imp * (c_ctr / 100))
        d_conv   = int(d_clicks * (c_cvr / 100))
        cum_conv += d_conv

        labels.append(f'D{d+1}')
        ctr_fc.append(c_ctr)
        cvr_fc.append(c_cvr)
        click_fc.append(d_clicks)
        conv_fc.append(cum_conv)

    return {
        'labels':    labels,
        'ctr':       ctr_fc,
        'cvr':       cvr_fc,
        'clicks':    click_fc,
        'cum_conv':  conv_fc,
    }
