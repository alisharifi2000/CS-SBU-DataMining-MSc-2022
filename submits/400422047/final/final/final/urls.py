"""final URL Configuration

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
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

import final.views as views

schema_view = get_schema_view(
   openapi.Info(
      title="Finals API",
      default_version='v1',
      description="For final project of Data Mining Course ",
      contact=openapi.Contact(email="bahary.yeganeh@gmail.com"),
   ),
   public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('HW1/', views.HW1View.as_view()),

    path('HW2/', views.HW2View.as_view()),

    path('HW3/', views.HW3View.as_view()),

    path('HW4/', views.HW4View.as_view()),

    path('', schema_view.with_ui('swagger', cache_timeout=0)),

]
