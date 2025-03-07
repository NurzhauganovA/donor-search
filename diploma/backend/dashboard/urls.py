from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('schedule-blood-donation/<int:pk>/', views.schedule_blood_donation, name='schedule_blood_donation'),

    path('api/create_donation_request/', views.create_donation_request, name='create_donation_request'),
]
