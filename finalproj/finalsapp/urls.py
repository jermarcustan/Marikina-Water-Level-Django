from django.urls import path
from . import views

app_name = "finalsapp"

urlpatterns = [
    path("", views.index, name ='welcome'),

    path("new/", views.add_record, name='add-record'),

    path("edit/<int:pk>/", views.update_record, name='update-record'),

    path("delete/<int:pk>/", views.delete_record, name='delete-record'),

    path("records/<int:pg>/", views.list_records, name='list-records'),

    path("datetimes/<int:pk>/", views.datetime_detail, name='datetime-detail'),

    path("queries/", views.query_records, name='query-records')
]