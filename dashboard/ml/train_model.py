"""
train_model.py
==============
Trains Random Forest (CTR) and Gradient Boosting (Conversion Rate) models.

Dataset:
  Social Media Ad Dataset — Kaggle
  https://www.kaggle.com/datasets/ziya07/social-media-ad-dataset
  (User Engagement, Ad Performance, Conversion Tracking — 2025)

Usage:
  # Train on synthetic data (no CSV needed):
  python dashboard/ml/train_model.py

  # Train on downloaded Kaggle CSV:
  python dashboard/ml/train_model.py path/to/social_media_ads.csv

Models saved to:  dashboard/ml/saved_models/
"""

import os
import sys
import math
import joblib
import numpy as np
import pandas as pd
from pathlib import Path

from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

SAVE_DIR = Path(__file__).parent / 'saved_models'
SAVE_DIR.mkdir(exist_ok=True)

CAT_FEATS = ['platform', 'ad_format', 'objective', 'industry']
NUM_FEATS = ['daily_budget', 'audience_size', 'duration_days']
ALL_FEATS = CAT_FEATS + NUM_FEATS


# ─── Synthetic data generator ─────────────────────────────────────────────────
def make_synthetic(n=10000, seed=42):
    """
    Generates realistic ad campaign data.
    Replace with Kaggle CSV loading for production.

    Dataset schema mirrors:
      https://www.kaggle.com/datasets/ziya07/social-media-ad-dataset
    """
    rng = np.random.default_rng(seed)

    PLATS = ['facebook', 'instagram', 'tiktok', 'linkedin', 'twitter']
    FMTS  = ['video', 'story', 'carousel', 'image', 'text']
    OBJS  = ['conversions', 'traffic', 'leads', 'awareness']
    INDS  = ['ecomm', 'saas', 'fin', 'health', 'edu']

    # Base CTR (%) per platform — sourced from industry benchmarks
    BASE_CTR = {'facebook':3.2,'instagram':3.8,'tiktok':4.6,'linkedin':2.0,'twitter':1.8}
    # Format multipliers (learned from ad platform analytics)
    FMT_MUL  = {'video':1.25,'story':1.20,'carousel':1.10,'image':0.95,'text':0.80}
    # Objective multipliers
    OBJ_MUL  = {'conversions':1.15,'leads':1.05,'traffic':1.0,'awareness':0.85}
    # Industry multipliers
    IND_MUL  = {'ecomm':1.08,'saas':0.95,'fin':1.0,'health':1.12,'edu':0.92}
    # Base conversion rate (%)
    BASE_CVR = {'facebook':15.0,'instagram':14.0,'tiktok':10.0,'linkedin':20.0,'twitter':8.0}

    rows = []
    for _ in range(n):
        p = rng.choice(PLATS); f = rng.choice(FMTS)
        o = rng.choice(OBJS);  i = rng.choice(INDS)
        bud = float(rng.uniform(50, 5000))
        aud = int(rng.integers(10_000, 5_000_000))
        dur = int(rng.integers(1, 91))

        # CTR: base × format × obj × industry × budget-log × duration-decay × noise
        bud_f = 1 + math.log10(max(bud, 50) / 50) * 0.04
        dur_f = 1.0 if dur <= 14 else 1.0 - (dur - 14) * 0.003
        aud_f = 1 - min(0.08, math.log10(max(aud, 1e4) / 1e4) * 0.015)

        ctr = (BASE_CTR[p] * FMT_MUL[f] * OBJ_MUL[o] * IND_MUL[i]
               * bud_f * dur_f * aud_f
               * rng.normal(1.0, 0.10))
        cvr = (BASE_CVR[p] * OBJ_MUL[o] * IND_MUL[i] * bud_f
               * rng.normal(1.0, 0.12))

        rows.append({
            'platform': p, 'ad_format': f, 'objective': o, 'industry': i,
            'daily_budget': round(bud, 2),
            'audience_size': aud,
            'duration_days': dur,
            'ctr': max(0.1, round(ctr, 4)),
            'conversion_rate': max(0.5, round(cvr, 4)),
        })

    return pd.DataFrame(rows)


# ─── Kaggle CSV loader ─────────────────────────────────────────────────────────
def load_kaggle(path):
    """
    Load the Kaggle 'Social Media Ad Dataset'.
    Adjust column_map to match actual CSV headers after download.
    """
    df = pd.read_csv(path)
    column_map = {
        # Kaggle column   → our schema
        'Platform':        'platform',
        'Ad_Type':         'ad_format',
        'Campaign_Goal':   'objective',
        'Industry':        'industry',
        'Budget':          'daily_budget',
        'Audience_Size':   'audience_size',
        'Duration':        'duration_days',
        'CTR':             'ctr',
        'Conversion_Rate': 'conversion_rate',
    }
    df = df.rename(columns=column_map)
    for c in CAT_FEATS:
        if c in df.columns:
            df[c] = df[c].str.lower().str.strip().str.replace(' ', '_')
    return df[ALL_FEATS + ['ctr', 'conversion_rate']].dropna()


# ─── Preprocessor ─────────────────────────────────────────────────────────────
def make_preprocessor():
    return ColumnTransformer([
        ('cat', Pipeline([('ohe', OneHotEncoder(handle_unknown='ignore', sparse_output=False))]), CAT_FEATS),
        ('num', Pipeline([('scl', StandardScaler())]),                                           NUM_FEATS),
    ])


# ─── Train & save ─────────────────────────────────────────────────────────────
def train(csv_path=None):
    print('\n' + '='*60)
    print('  Social Media Ad — ML Training Pipeline')
    print('='*60)

    # 1. Data
    if csv_path and os.path.exists(csv_path):
        print(f'\n[1/5] Loading Kaggle CSV: {csv_path}')
        df = load_kaggle(csv_path)
    else:
        print('\n[1/5] Generating synthetic training data (10 000 samples)…')
        df = make_synthetic(10000)

    print(f'      Shape: {df.shape}')

    X = df[ALL_FEATS]
    y_ctr = df['ctr']
    y_cvr = df['conversion_rate']

    # 2. Split
    print('\n[2/5] Train / test split (80 / 20)…')
    X_tr, X_te, yc_tr, yc_te = train_test_split(X, y_ctr, test_size=0.2, random_state=42)
    _,    _,    yv_tr, yv_te = train_test_split(X, y_cvr, test_size=0.2, random_state=42)

    # 3. Models
    print('\n[3/5] Building pipelines…')
    ctr_pipe = Pipeline([
        ('pre', make_preprocessor()),
        ('rf',  RandomForestRegressor(
            n_estimators=300, max_depth=14,
            min_samples_leaf=4, max_features='sqrt',
            random_state=42, n_jobs=-1,
        )),
    ])
    cvr_pipe = Pipeline([
        ('pre', make_preprocessor()),
        ('gb',  GradientBoostingRegressor(
            n_estimators=300, max_depth=5,
            learning_rate=0.04, subsample=0.8,
            random_state=42,
        )),
    ])

    # 4. Fit & evaluate
    print('\n[4/5] Training…')

    ctr_pipe.fit(X_tr, yc_tr)
    ctr_pred = ctr_pipe.predict(X_te)
    print(f'      CTR  Model → MAE={mean_absolute_error(yc_te,ctr_pred):.4f}  '
          f'RMSE={mean_squared_error(yc_te,ctr_pred)**.5:.4f}  R²={r2_score(yc_te,ctr_pred):.4f}')

    cvr_pipe.fit(X_tr, yv_tr)
    cvr_pred = cvr_pipe.predict(X_te)
    print(f'      CVR  Model → MAE={mean_absolute_error(yv_te,cvr_pred):.4f}  '
          f'RMSE={mean_squared_error(yv_te,cvr_pred)**.5:.4f}  R²={r2_score(yv_te,cvr_pred):.4f}')

    # 5-fold CV on CTR
    cv_scores = cross_val_score(ctr_pipe, X, y_ctr, cv=5, scoring='r2')
    print(f'      CTR  5-Fold CV R² = {cv_scores.mean():.4f} ± {cv_scores.std():.4f}')

    # Feature importance
    ohe        = ctr_pipe.named_steps['pre'].named_transformers_['cat']['ohe']
    cat_names  = ohe.get_feature_names_out(CAT_FEATS).tolist()
    all_names  = cat_names + NUM_FEATS
    raw_imp    = ctr_pipe.named_steps['rf'].feature_importances_

    # Aggregate back to original features
    feat_imp = {}
    for name, imp in zip(all_names, raw_imp):
        root = name.split('_')[0]
        feat_imp[root] = feat_imp.get(root, 0) + imp

    # Round & sort
    feat_imp = {k: round(v, 4) for k, v in sorted(feat_imp.items(), key=lambda x: -x[1])}

    print('\n      Feature Importances (CTR model):')
    for k, v in feat_imp.items():
        bar = '█' * int(v * 50)
        print(f'        {k:<15} {bar}  {v:.4f}')

    # 5. Save
    print(f'\n[5/5] Saving to {SAVE_DIR}…')
    joblib.dump(ctr_pipe,  SAVE_DIR / 'ctr_model.pkl')
    joblib.dump(cvr_pipe,  SAVE_DIR / 'cvr_model.pkl')
    joblib.dump(feat_imp,  SAVE_DIR / 'feature_importance.pkl')
    print('      ✓ ctr_model.pkl')
    print('      ✓ cvr_model.pkl')
    print('      ✓ feature_importance.pkl')
    print('\n  Done!\n')


if __name__ == '__main__':
    train(sys.argv[1] if len(sys.argv) > 1 else None)
