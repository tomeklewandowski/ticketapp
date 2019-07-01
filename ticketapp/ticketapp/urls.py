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

from django.contrib import admin
from django.urls import path, include
from ticket_app.views import AddEventView
from ticket_app.views import EventList
from rest_framework import routers
from ticket_app.views import EventViewSet

router = routers.DefaultRouter()
router.register(r'list_events', EventViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('addevent', AddEventView.as_view(), name="addevent"),
    path('list_events', EventList.as_view(), name="list_events")
]
