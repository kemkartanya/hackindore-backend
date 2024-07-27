from django.urls import path, include
from rest_framework import routers

from .views import TicketViewSet

router = routers.DefaultRouter()
router.register("ticket", TicketViewSet, basename="ticket")


urlpatterns = [
    path("", include(router.urls)),
]
