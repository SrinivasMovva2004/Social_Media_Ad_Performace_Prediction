from django.urls import path
from . import views

urlpatterns = [
    # Pages
    path('', views.index, name='index'),

    # REST API endpoints
    path('api/kpis/',               views.api_kpis,               name='api-kpis'),
    path('api/platform-stats/',     views.api_platform_stats,     name='api-platform-stats'),
    path('api/predict/',            views.api_predict,            name='api-predict'),
    path('api/prediction-history/', views.api_prediction_history, name='api-prediction-history'),
]
