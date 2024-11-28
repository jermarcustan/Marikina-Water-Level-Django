from django.urls import path
from . import views

app_name = 'hopesdreams'
urlpatterns = [
    # localhost:8000/hopesdreams/
    path('', views.index),

    
    # localhost:8000/hopesdreams/dreamer/new/

    path('dreamer/new/', views.adddreamer, name = 'dreamer-add'),

    # localhost:8000/hopesdreams/dreamers/

    path('dreamers/', views.listdreamer, name = 'dreamer-list'),

    # localhost:8000/hopesdreams/dreamer/<id>/
    
    path('dreamer/<int:pk>/', views.detaildreamer, name = 'dreamer-detail'),


]