from django.urls import path, include
from rest_framework import routers

from .views import DocumentViewSet

router = routers.DefaultRouter()
router.register("document", DocumentViewSet, basename="document")


urlpatterns = [
    path("", include(router.urls)),
]
