from django.core.wsgi import get_wsgi_application
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ad_performance_system.settings')
application = get_wsgi_application()
