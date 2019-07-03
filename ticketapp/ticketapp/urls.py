from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from ticket_app.views import EventListViewSet, AvailableTicketsViewSet, ReservationViewSet, EventViewSet, Stats, AddEventView


router = routers.DefaultRouter()
router.register(r'api/list_events', EventViewSet, basename='EventViewSet')
#router.register(r'api/available_tickets', AvailableTicketsViewSet, basename='AvailableTicketsViewSet')
#router.register(r'api/reservation', ReservationViewSet, basename='ReservationViewSet')


urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', include(router.urls)),
    path(r'api/', include('rest_framework.urls', namespace='rest_framework')),
    path('addevent', AddEventView.as_view(), name='addevent'),
    path('available_tickets/<int:event_id>/', AvailableTicketsViewSet.as_view(), name='available_tickets'),
    path('reservation/<int:event_id>/<int:ticket_type>/', ReservationViewSet.as_view(), name='reservation'),
    path('stats', Stats.as_view(), name='stats'),
]

