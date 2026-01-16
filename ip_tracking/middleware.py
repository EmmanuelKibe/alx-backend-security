from .models import RequestLog, BlockedIP
from django.http import HttpResponseForbidden
import ipinfo
from django.core.cache import cache
from django.conf import settings

class IPTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.handler = ipinfo.getHandler(getattr(settings, 'IPINFO_TOKEN', None))

    def __call__(self, request):
        # Extract IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        # Create the log entry in the database
        if ip:
            #Check if the IP is blocked
            if BlockedIP.objects.filter(ip_address=ip).exists():
                return HttpResponseForbidden("Access Denied: Your IP has been blacklisted.")

            cache_key = f"geo_{ip}"
            geo_data = cache.get(cache_key)

            if not geo_data:
                try:
                    #Call API if not in cache
                    details = self.handler.getDetails(ip)
                    geo_data = {
                        'country': details.country_name,
                        'city': details.city
                    }
                    # Cache for 24 hours (86400 seconds)
                    cache.set(cache_key, geo_data, 86400)
                except Exception:
                    geo_data = {'country': 'Unknown', 'city': 'Unknown'}

            RequestLog.objects.create(
                ip_address=ip,
                path=request.path,
                country=geo_data.get('country'),
                city=geo_data.get('city')
            )

        response = self.get_response(request)
        return response
