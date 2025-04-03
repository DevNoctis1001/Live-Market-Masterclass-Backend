"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from apps.alerts.views import main

from django.shortcuts import redirect  # Add this import

# def redirect_to_admin(request):
#     return redirect('admin:index')

urlpatterns = [
    # path('', "Hello ", name='home'),  # Add this line
    path('', main, name = "FetchEmail"),
    path('admin/', admin.site.urls), 
    # path('gmail_webhook/', gmail_webhook),  # Add this line to include the webhook URL
    # path('api/telegram/', handle_telegram_update, name='telegram_webhook')
    
]
