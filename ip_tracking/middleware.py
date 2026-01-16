from .models import RequestLog, BlockedIP

class IPTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

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

            RequestLog.objects.create(
                ip_address=ip,
                path=request.path
            )

        response = self.get_response(request)
        return response
