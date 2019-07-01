"""ticketapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path
from ticket_app.views import AddEventView, LoginView, logout_view, MainView
from django.contrib.auth import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name="main"),
    path('login', LoginView.as_view(), name="login"),
    path('logout', logout_view, name="logout" ),
    path('register', RegisterView.as_view(), name="register"),
    path('addevent', AddEventView.as_view(), name="addevent"),
]
