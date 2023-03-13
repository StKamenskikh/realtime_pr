from django.urls import path
from .views import index1, index, index2

urlpatterns = [
    path('', index1),
    path('index', index)
]