from django.urls import path
from . import views


urlpatterns= [
    path('news/', views.newslist,name='newslist'),
    path('contact/', views.contact_view,name='contact_view'),
    path('prices/', views.priceslist, name='priceslist'),
    path('trainers/', views.trainerslist, name='trainerslist'),
    path('schedule_view/', views.schedule_view, name='schedule_view'),
    path('enroll/', views.enroll, name='enroll'),

]