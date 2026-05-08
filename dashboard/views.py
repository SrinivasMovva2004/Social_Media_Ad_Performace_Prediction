import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import AdCampaign, PredictionLog
from .ml.predict import predict as ml_predict


# ─── Pages ────────────────────────────────────────────────────────────────────

def index(request):
    """Render the main dashboard SPA."""
    return render(request, 'dashboard/index.html')


# ─── API: Dashboard KPIs ──────────────────────────────────────────────────────

@api_view(['GET'])
def api_kpis(request):
    """Return aggregated dashboard KPIs."""
    campaigns = AdCampaign.objects.all()
    if not campaigns.exists():
        # Return demo data when DB is empty
        return Response({
            'avg_ctr':         3.42,
            'total_conversions': 12840,
            'total_impressions': 2100000,
            'avg_roas':          4.2,
            'campaigns':         0,
        })

    total_imp   = sum(c.impressions for c in campaigns)
    total_clk   = sum(c.clicks for c in campaigns)
    total_conv  = sum(c.conversions for c in campaigns)
    total_spend = sum(c.spend for c in campaigns)
    total_rev   = sum(c.revenue for c in campaigns)
    avg_ctr     = round((total_clk / total_imp * 100) if total_imp else 0, 2)
    avg_roas    = round((total_rev / total_spend) if total_spend else 0, 2)

    return Response({
        'avg_ctr':           avg_ctr,
        'total_conversions': total_conv,
        'total_impressions': total_imp,
        'avg_roas':          avg_roas,
        'campaigns':         campaigns.count(),
    })


# ─── API: Platform breakdown ──────────────────────────────────────────────────

@api_view(['GET'])
def api_platform_stats(request):
    """CTR, conversions, spend per platform."""
    platforms = ['facebook', 'instagram', 'tiktok', 'linkedin', 'twitter']
    demo = {
        'facebook':  {'ctr': 3.42, 'conversions': 3840, 'spend': 8400,  'impressions': 420000},
        'instagram': {'ctr': 4.10, 'conversions': 4200, 'spend': 9200,  'impressions': 510000},
        'tiktok':    {'ctr': 4.82, 'conversions': 2100, 'spend': 5800,  'impressions': 380000},
        'linkedin':  {'ctr': 2.15, 'conversions': 1900, 'spend': 7200,  'impressions': 290000},
        'twitter':   {'ctr': 1.72, 'conversions':  800, 'spend': 2100,  'impressions': 200000},
    }

    if AdCampaign.objects.exists():
        result = {}
        for p in platforms:
            qs = AdCampaign.objects.filter(platform=p)
            if qs.exists():
                ti = sum(c.impressions for c in qs)
                tc = sum(c.clicks for c in qs)
                result[p] = {
                    'ctr':         round((tc / ti * 100) if ti else 0, 2),
                    'conversions': sum(c.conversions for c in qs),
                    'spend':       round(sum(c.spend for c in qs), 2),
                    'impressions': ti,
                }
        return Response(result)

    return Response(demo)


# ─── API: ML Prediction ───────────────────────────────────────────────────────

@csrf_exempt
@api_view(['POST'])
def api_predict(request):
    """
    POST /api/predict/
    Body (JSON):
        platform, ad_format, objective, industry,
        daily_budget, audience_size, duration_days
    """
    data = request.data

    required = ['platform', 'ad_format', 'objective', 'industry',
                'daily_budget', 'audience_size', 'duration_days']
    for field in required:
        if field not in data:
            return Response({'error': f'Missing field: {field}'},
                            status=status.HTTP_400_BAD_REQUEST)

    try:
        result = ml_predict(
            platform=data['platform'],
            ad_format=data['ad_format'],
            objective=data['objective'],
            industry=data['industry'],
            daily_budget=float(data['daily_budget']),
            audience_size=int(data['audience_size']),
            duration_days=int(data['duration_days']),
        )
    except FileNotFoundError as e:
        return Response({'error': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    except Exception as e:
        return Response({'error': f'Prediction failed: {e}'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Log the prediction
    PredictionLog.objects.create(
        platform=data['platform'],
        ad_format=data['ad_format'],
        objective=data['objective'],
        industry=data['industry'],
        daily_budget=float(data['daily_budget']),
        audience_size=int(data['audience_size']),
        duration_days=int(data['duration_days']),
        predicted_ctr=result['predicted_ctr'],
        predicted_conv_rate=result['predicted_cvr'],
        predicted_clicks=result['predicted_clicks'],
        predicted_conversions=result['predicted_conversions'],
        predicted_roas=result['predicted_roas'],
        confidence_score=result['confidence_score'],
    )

    return Response(result)


# ─── API: Recent predictions ──────────────────────────────────────────────────

@api_view(['GET'])
def api_prediction_history(request):
    logs = PredictionLog.objects.all()[:20]
    data = [{
        'platform':     l.platform,
        'ad_format':    l.ad_format,
        'predicted_ctr': l.predicted_ctr,
        'predicted_conversions': l.predicted_conversions,
        'confidence_score': l.confidence_score,
        'created_at':   l.created_at.strftime('%Y-%m-%d %H:%M'),
    } for l in logs]
    return Response(data)
