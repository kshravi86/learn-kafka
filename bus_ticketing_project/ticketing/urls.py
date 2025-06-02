from django.urls import path
from .views import (
    BusListView,
    BusDetailView,
    BusCreateView,
    BusUpdateView,
    BusDeleteView
)

urlpatterns = [
    path('', BusListView.as_view(), name='bus_list'),
    path('bus/<int:pk>/', BusDetailView.as_view(), name='bus_detail'),
    path('bus/new/', BusCreateView.as_view(), name='bus_create'),
    path('bus/<int:pk>/edit/', BusUpdateView.as_view(), name='bus_update'),
    path('bus/<int:pk>/delete/', BusDeleteView.as_view(), name='bus_delete'),
]
