from django.urls import path
from .views import check_dev_status, index, switch_detail

app_name = "Dashboard"
urlpatterns = [
    path("", index.as_view(), name="observation_list"),
    path('check_dev_status/', check_dev_status, name='check_dev_status'),
    path('switches/<int:dev_id>/', switch_detail, name='switch_detail'),
]
