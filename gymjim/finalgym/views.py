from django.shortcuts import render, redirect
from django.views import View
from .models import  News
from django.http import HttpResponse
def newslist(request):
    news=News.objects.all()
    return render(request,'news_list.html', {'news': news})




