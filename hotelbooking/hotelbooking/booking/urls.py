from django.urls import path
from . import views

urlpatterns=[
    path('home/',views.home,name='home'),
    path('login/',views.login_page,name='login'),
    path('register/',views.regsiter_page,name='register'),
    path('hoteldetail/<uid>/',views.hoteldetail,name='hotel-detail'),
    path('check_booking/',views.check_booking)
]