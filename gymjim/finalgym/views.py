from django.shortcuts import render, redirect
from django.views import View
from .models import News, Contact, Price, Trainer, Schedule, Enroll, Exercise, Message
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse


def logout_view(request):
    logout(request)
    login_url = reverse('home')
    return redirect(login_url)


def home(request):
    return render(request, 'home.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message='Invalid username or password!'
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html',{'form': form})


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
    trainers = Trainer.objects.all()
    return render(request,'trainers.html', {'trainers': trainers})


def schedule_view(request):
    schedule = Schedule.objects.all()
    return render(request, 'schedule.html', {'schedule': schedule})


@login_required
def enroll(request,exercise_id):
    exercise = Exercise.objects.get(id=exercise_id)
    is_enrolled = Enroll.objects.filter(user=request.user, exercise=exercise).exists()

    if is_enrolled:
        message = "You are already registred for classes!"

    else:
        Enroll.objects.create(user=request.user, exercise=exercise)
        message = "You have been enrolled for classes!"

    return render(request, 'enroll.html', {'message': message})


@login_required
def user_profile(request):
    user = request.user
    exercises = Exercise.objects.filter(enroll__user=user)
    messages = Message.objects.filter(recipient=user)

    if request.method == 'POST':
        exercise_id = request.POST.get('exercise_id')
        enroll = Enroll.objects.get(user=user, exercise_id=exercise_id)
        enroll.delete()
        return redirect(reverse('user_profile'))

    context = {
        'exercises': exercises,
        'messages': messages,
    }

    return render(request, 'user_profile.html', context)