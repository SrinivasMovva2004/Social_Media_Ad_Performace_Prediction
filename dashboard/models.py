from django.db import models


class AdCampaign(models.Model):
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'), ('instagram', 'Instagram'),
        ('tiktok', 'TikTok'), ('linkedin', 'LinkedIn'), ('twitter', 'X / Twitter'),
    ]
    FORMAT_CHOICES = [
        ('video', 'Video'), ('story', 'Story / Reel'), ('carousel', 'Carousel'),
        ('image', 'Static Image'), ('text', 'Text / Sponsored'),
    ]
    OBJECTIVE_CHOICES = [
        ('conversions', 'Conversions'), ('traffic', 'Traffic'),
        ('leads', 'Lead Generation'), ('awareness', 'Brand Awareness'),
    ]
    INDUSTRY_CHOICES = [
        ('ecomm', 'E-Commerce'), ('saas', 'SaaS / Tech'), ('fin', 'Finance'),
        ('health', 'Health & Wellness'), ('edu', 'Education'),
    ]

    campaign_name = models.CharField(max_length=200)
    platform      = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    ad_format     = models.CharField(max_length=20, choices=FORMAT_CHOICES)
    objective     = models.CharField(max_length=20, choices=OBJECTIVE_CHOICES)
    industry      = models.CharField(max_length=20, choices=INDUSTRY_CHOICES)

    daily_budget  = models.FloatField()
    audience_size = models.IntegerField()
    duration_days = models.IntegerField()
    start_date    = models.DateField()

    impressions   = models.IntegerField(default=0)
    clicks        = models.IntegerField(default=0)
    conversions   = models.IntegerField(default=0)
    spend         = models.FloatField(default=0.0)
    revenue       = models.FloatField(default=0.0)

    # Computed
    ctr             = models.FloatField(default=0.0)
    conversion_rate = models.FloatField(default=0.0)
    cpc             = models.FloatField(default=0.0)
    roas            = models.FloatField(default=0.0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']

    def save(self, *args, **kwargs):
        if self.impressions > 0:
            self.ctr = round((self.clicks / self.impressions) * 100, 4)
        if self.clicks > 0:
            self.conversion_rate = round((self.conversions / self.clicks) * 100, 4)
            self.cpc = round(self.spend / self.clicks, 4)
        if self.spend > 0:
            self.roas = round(self.revenue / self.spend, 4)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.campaign_name} | {self.platform} | {self.start_date}"


class PredictionLog(models.Model):
    platform      = models.CharField(max_length=20)
    ad_format     = models.CharField(max_length=20)
    objective     = models.CharField(max_length=20)
    industry      = models.CharField(max_length=20)
    daily_budget  = models.FloatField()
    audience_size = models.IntegerField()
    duration_days = models.IntegerField()

    predicted_ctr         = models.FloatField()
    predicted_conv_rate   = models.FloatField()
    predicted_clicks      = models.IntegerField()
    predicted_conversions = models.IntegerField()
    predicted_roas        = models.FloatField()
    confidence_score      = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.platform} | CTR:{self.predicted_ctr} | {self.created_at:%Y-%m-%d %H:%M}"
