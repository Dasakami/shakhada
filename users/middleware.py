from django.shortcuts import redirect, render
from django.urls import reverse
from django.conf import settings

from django.shortcuts import render
from .models import MaintenanceStatus

class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # суперпользователи не видят техработы
        if hasattr(request, 'user') and request.user.is_authenticated and request.user.is_superuser:
            return self.get_response(request)

        # Проверка из базы
        status = MaintenanceStatus.objects.first()
        if status and status.is_active:
            return render(request, 'users/maintenance.html')

        return self.get_response(request)

