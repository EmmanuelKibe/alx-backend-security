from django.shortcuts import render
from django.http import HttpResponse
from django_ratelimit.decorators import ratelimit

# This function determines the rate based on authentication status
def get_rate(group, request):
    if request.user.is_authenticated:
        return '10/m'  # 10 requests per minute for logged-in users
    return '5/m'       # 5 requests per minute for anonymous users

@ratelimit(key='ip', rate=get_rate, method='ALL', block=True)
def sensitive_login_view(request):
    return HttpResponse("Welcome to the Login Page. Please enter your credentials.")


