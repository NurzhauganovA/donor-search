from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('schedule-blood-donation/<int:pk>/', views.schedule_blood_donation, name='schedule_blood_donation'),
    path('how_become_donor', views.how_become_donor, name='how_become_donor'),
    path('bloodstations', views.where_donate_blood, name='where_donate_blood'),
    path('requirements', views.base_requirements, name='base_requirements'),

    path('bloodstations/<str:city_name>', views.bloodstations_detail_city, name='bloodstations_detail_city'),

    path('urgently-need-donor', views.urgently_need_donor, name='urgently_need_donor'),
    path('urgently-need-donor/search', views.search_urgently_need_donor, name='search_urgently_need_donor'),
    path('urgently-need-donor/<int:pk>', views.urgently_donor_detail, name='urgently_donor_detail'),
    path('schedule_request_blood_donation/<int:pk>', views.schedule_request_blood_donation, name='schedule_request_blood_donation'),

    path('api/create_urgently_donor_request/', views.create_urgently_donor_request, name='create_urgently_donor_request'),
    path('api/create_donation_request/', views.create_donation_request, name='create_donation_request'),

    path('api/get_unique_cities/', views.get_unique_cities, name='get_unique_cities'),
    path('api/get_blood_donation_centers_by_city/', views.get_blood_donation_centers_by_city, name='get_blood_donation_centers_by_city'),

    path('donate/', views.donate, name='donate'),
]
