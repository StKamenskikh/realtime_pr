from django.urls import path

from .consumers import WSConsumer, DataConsumer

ws_urlpatterns = [
    path('ws/some_url/', WSConsumer.as_asgi()),
    path('ws/tags=<tags>/',DataConsumer.as_asgi()),
]