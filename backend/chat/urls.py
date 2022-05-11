from site import venv
from django.urls import path
from .views import index, HelloApiView

urlpatterns = [
    path('', index, name='index'),
    path('hello/', HelloApiView.as_view(), name='hello'),
]
