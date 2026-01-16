from django.contrib import admin
from .models import RequestLog, BlockedIP

# Register your models here.
admin.site.register(RequestLog)
admin.site.register(BlockedIP)

