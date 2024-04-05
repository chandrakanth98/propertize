"""
URL configuration for propertize project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from properties import views as p_views

urlpatterns = [
    path("finance/", include("finance.urls"), name="finances"),
    path("maintenance/", include("maintenance.urls"), name="requests"),
    path("tenants/", include("tenants.urls"), name="tenants"),
    path("properties/", include("properties.urls"), name="properties"),
    path("", include("dashboards.urls")),
    path("accounts/", include("allauth.urls")),
    path("stripe/", include("djstripe.urls", namespace="djstripe")),
    path('admin/', admin.site.urls),
]
