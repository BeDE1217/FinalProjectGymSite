from django.shortcuts import render, redirect
from django.views import View
from .models import News, Contact
from django.http import HttpResponse


def newslist(request):

    news = News.objects.all()
    return render(request, 'news_list.html', {'news': news})




def contact_view(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        topic = request.POST.get('topic')
        message = request.POST.get('message')

        contact = Contact.objects.create(email=email, phone=phone, topic=topic, message=message)

        return render(request,'news_list.html')


    phonenumber = "tel: +48 123 456 786"
    bankaccount = " 4503 34560 3560 33556 35501"
    address = "Siłowniowa 9/10 Kraków, schodami do góry"
    emailgym = "gymjim@ggmail.ccom"

    return render(request, 'contact.html',
                  {'phonenumber': phonenumber, 'emailgym': emailgym, 'bankaccount': bankaccount, 'address': address})