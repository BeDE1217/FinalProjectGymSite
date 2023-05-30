from django.shortcuts import render, redirect
from django.views import View
from .models import News, Contact, Price, Trainer, Schedule, Enroll, Exercise
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


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

        return render(request,'contact success.html')


    phonenumber = "tel: +48 123 456 786"
    bankaccount = " 4503 34560 3560 33556 35501"
    address = "Siłowniowa 9/10 Kraków, schodami do góry"
    emailgym = "gymjim@ggmail.ccom"

    return render(request, 'contact.html',
                  {'phonenumber': phonenumber, 'emailgym': emailgym, 'bankaccount': bankaccount, 'address': address})


def priceslist(request):
    prices = Price.objects.all()
    return render(request, 'prices.html', {'prices': prices})


def trainerslist(request):
    trainers= Trainer.objects.all()
    return render(request,'trainers.html', {'trainers': trainers})

@login_required
def schedule_view(request):
    schedule = Schedule.objects.all()
    enroll_exercises= Enroll.objects.filter(user=request.user)
    enroll_exercise_ids= [enroll.exercise.id for enroll in enroll_exercises]
    return render(request, 'schedule.html', {'schedule': schedule,'enroll_exercies_ids': enroll_exercise_ids})

@login_required
def enroll(request):
   if request.method == 'POST':
       exercise_id = request.POST.get('exercise_id')
       exercise= Exercise.objects.get(id=exercise_id)
       is_enrolled= Enroll.objects.filter(user=request.user, exercise=exercise). exists()

       if is_enrolled:
           message = "Jesteś już zapisany/a na zajęcia!"
       else:
           Enroll.objects.create(user=request.user, exercise=exercise)
           message= "Zostałeś/aś zapisany/a na zajecią!"
       return render(request, 'enroll.html', {'message': message})

   return redirect('schedule_view')