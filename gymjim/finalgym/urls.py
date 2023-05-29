from django.urls import path
from . import views


urlpatterns= [
    path('news/',views.newslist,name='newslist'),
    path('contact/',views.contact_view,name='contact_view' )
]