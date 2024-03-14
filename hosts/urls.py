from django.urls import path

from .views import HostView

urlpatterns = [
    path('search', HostView.as_view())
]
