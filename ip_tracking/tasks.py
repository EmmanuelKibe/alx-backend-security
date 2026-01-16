from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from .models import RequestLog, SuspiciousIP

@shared_task
def detect_anomalies():
    one_hour_ago = timezone.now() - timedelta(hours=1)
    
    # 1. Flag IPs with > 100 requests in the last hour
    high_volume_ips = (
        RequestLog.objects.filter(timestamp__gte=one_hour_ago)
        .values('ip_address')
        .annotate(total=Count('id'))
        .filter(total__gt=100)
    )
    
    for entry in high_volume_ips:
        SuspiciousIP.objects.get_or_create(
            ip_address=entry['ip_address'],
            reason=f"High volume: {entry['total']} requests/hour"
        )

    # 2. Flag IPs accessing sensitive paths
    sensitive_paths = ['/admin', '/login', '/wp-admin', '/.env']
    suspicious_path_logs = RequestLog.objects.filter(
        timestamp__gte=one_hour_ago,
        path__in=sensitive_paths
    ).values('ip_address', 'path').distinct()

    for log in suspicious_path_logs:
        SuspiciousIP.objects.get_or_create(
            ip_address=log['ip_address'],
            reason=f"Accessed sensitive path: {log['path']}"
        )