from django.contrib import admin
from .models import RequestLog, BlockedIP

# Register your models here.
from django.contrib import admin
from .models import RequestLog, BlockedIP

@admin.register(RequestLog)
class RequestLogAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'country', 'city', 'path', 'timestamp')
    list_filter = ('country', 'timestamp')
    search_fields = ('ip_address', 'city')

@admin.register(BlockedIP)
class BlockedIPAdmin(admin.ModelAdmin):
    list_display = ('ip_address',)

