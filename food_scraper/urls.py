"""food_scraper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from input_data.views import form_view, scrape_view, signup_view, signin_view,signout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', form_view, name='form'),
    path('scrape/', scrape_view),
    path('signup/', signup_view),
    path('signin/', signin_view),
    path('signout/', signout_view),
    
]
