from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from vehicle.views import (
    VehicleListView,
    VehicleView,
    VehicleSetDriverView
)

urlpatterns = format_suffix_patterns(
    [
        path('vehicle/', VehicleListView.as_view(), name='vehicles'),
        path('vehicle/<int:vehicle_id>/', VehicleView.as_view(), name='vehicle'),
        path('set_driver/<int:vehicle_id>/', VehicleSetDriverView.as_view(), name='vehicle_set_driver')
    ]
)
