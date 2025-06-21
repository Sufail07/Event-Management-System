from django.urls import path, include
from .views import EventView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'events', EventView, basename='event')

urlpatterns = [
    path('', include(router.urls))
]
