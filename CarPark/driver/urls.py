from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from driver.views import DriverListView, DriverView

urlpatterns = format_suffix_patterns(
    [
        path('driver/', DriverListView.as_view(), name='drivers'),
        path('driver/<int:driver_id>/', DriverView.as_view(), name='driver'),
    ]
)
