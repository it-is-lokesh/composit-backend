from django.urls import path
from userdashboard import views

urlpatterns = [
    path('registerForEvent', views.registerForEvent, name='registerForEvent'),
]
