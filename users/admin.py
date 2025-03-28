from django.contrib import admin
from .models import User, Feedback
from .models import MaintenanceStatus
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'feedback_type', 'created_at')
    list_filter = ('feedback_type', 'created_at')
    search_fields = ('user__username', 'message')
admin.site.register(User)
admin.site.register(Feedback, FeedbackAdmin)
# Register your models here.

@admin.register(MaintenanceStatus)
class MaintenanceStatusAdmin(admin.ModelAdmin):
    list_display = ('is_active',)

