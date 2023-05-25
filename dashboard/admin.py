from django.contrib import admin
from .models import GeneralInfo, PerformanceMetrics, AdvancedInfo

# Register your models here.
admin.site.register(GeneralInfo)
admin.site.register(PerformanceMetrics)
admin.site.register(AdvancedInfo)
