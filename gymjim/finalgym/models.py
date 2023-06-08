from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.utils import timezone


class News(models.Model):
    """Model representing news in gym."""
    title = models.CharField(max_length=250)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)


class Exercise(models.Model):
    """Model representing an exercise."""
    name = models.CharField(max_length=225, blank=True)
    description = models.TextField()

    def __str__(self):
        return str(self.name)


class Schedule(models.Model):
    """Model representing a class schedule, linked to an exercise and trainer."""
    gym_class = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    trainer = models.ForeignKey('Trainer', on_delete=models.CASCADE)
    day = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return str(self.gym_class)


class Price(models.Model):
    """Model representing a price."""
    name = models.CharField(max_length=100, blank=True )
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)

    def __str__(self):
        return str(self.name)


class Trainer(models.Model):
    """Model representing a trainer, linked to exercises."""
    name = models.CharField(max_length=100, blank=True )
    bio = models.TextField()
    classes = models.ManyToManyField(Exercise, through='Schedule')

    def __str__(self):
        return str(self.name)


class Contact(models.Model):
    """Model representing contact form for users of website."""
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    topic = models.CharField(max_length=100, blank=True)
    message = models.TextField(blank=True)

    def __str__(self):
        return str(self.email)


class Enroll(models.Model):
    """Model representing an enrollment, linked to a user and exercise."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, default=None)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.user)


class Account(User):
    """Model representing a user account, extending a User model."""
    def __str__(self):
        return str(self.name)


class Message(models.Model):
    """Model representing a message, linked to a User model."""
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=100)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=True)

    def __str__(self):
        return str(self.subject)


