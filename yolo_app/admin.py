from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display    = ('created_at', 'count', 'original_image', 'result_image', 'pdf_report')
    list_filter     = ('created_at',)
    readonly_fields = ('created_at',)
