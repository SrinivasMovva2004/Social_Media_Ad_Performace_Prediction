from django.contrib import admin
from .models import AdCampaign, PredictionLog


@admin.register(AdCampaign)
class AdCampaignAdmin(admin.ModelAdmin):
    list_display  = ['campaign_name', 'platform', 'ad_format', 'objective',
                     'industry', 'daily_budget', 'ctr', 'conversion_rate', 'roas', 'start_date']
    list_filter   = ['platform', 'ad_format', 'objective', 'industry']
    search_fields = ['campaign_name']
    ordering      = ['-start_date']
    readonly_fields = ['ctr', 'conversion_rate', 'cpc', 'roas', 'created_at', 'updated_at']


@admin.register(PredictionLog)
class PredictionLogAdmin(admin.ModelAdmin):
    list_display = ['platform', 'ad_format', 'objective', 'industry',
                    'predicted_ctr', 'predicted_conversions', 'confidence_score', 'created_at']
    list_filter  = ['platform', 'objective']
    ordering     = ['-created_at']
    readonly_fields = list_display
