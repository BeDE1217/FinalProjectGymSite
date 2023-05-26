from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class News(models.Model):
    title = models.CharField(max_length=250)
    content= models.TextField()
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Exercise(models.Model):
    name=models.CharField(max_length=225, default='')
    description=models.TextField()

    def __str__(self):
        return self.name


class Schedule(models.Model):
    gym_class=models.ForeignKey(Exercise, on_delete=models.CASCADE)
    trainer=models.ForeignKey('Trainer',on_delete=models.CASCADE)
    day= models.DateField()
    time=models.TimeField()

    def __str__(self):
        return self.gym_class


class Price(models.Model):
    name=models.CharField(max_length=100, default='')
    amount=models.DecimalField(max_digits=8, decimal_places=2, default=0.0)

    def __str__(self):
        return self.name


class Trainer(models.Model):
    name=models.CharField(max_length=100, default='')
    bio= models.TextField()
    classes= models.ManyToManyField(Exercise, through='Schedule')

    def __str__(self):
        return self.name


class Contact(models.Model):
    email=models.EmailField(default='')
    phone=models.CharField(max_length=20, default='')
    #address=models.CharField(max_length=200, default='')
    #opening_hours=models.CharField(max_length=100, default='')
    message=models.TextField()

    def __str__(self):
        return str(self.email)


class Enroll(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE, default=None)
    exercise= models.ForeignKey(Exercise, on_delete=models.CASCADE, default=None)
    date=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.user)
