"""Interpolation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import include, path
from interpolation_1.views import interpolate, outlier, balance_data, convert_date_interpolate

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('interpolation-1', ),
    path('interpolation/', interpolate),
    path('interpolate-convert-date/', convert_date_interpolate),
    path('outliers/', outlier),
    path('balance-data/', balance_data),
]
