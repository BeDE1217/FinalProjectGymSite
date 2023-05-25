from django.shortcuts import render, redirect
from django.views import View
from .models import  News

def newslist(request):
    news=News.objects.all()




