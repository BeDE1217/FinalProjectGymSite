from django.test import TestCase
from django.urls import reverse
from .models import News, Schedule, Exercise, Trainer, Enroll, Contact
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import date, time
from django.contrib.auth import authenticate, login


class NewsListViewTestCase(TestCase):
    def setUp(self):
        self.news1 = News.objects.create(title="message1", content="message test1")
        self.news2 = News.objects.create(title="message2", content="message test2")

    def test_news_list_view(self):
        response = self.client.get(reverse('newslist'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['news']), 2)
        self.assertIn(self.news1, response.context['news'])
        self.assertIn(self.news2, response.context['news'])


class ScheduleTestCase(TestCase):
    def setUp(self):
        self.exercise = Exercise.objects.create(name='Exercise1', description='description1test')
        self.trainer = Trainer.objects.create(name='Trainer1', bio='bio1test')
        self.schedule = Schedule.objects.create(gym_class=self.exercise, trainer=self.trainer, day=date.today(),
                                                time=time(hour=10, minute=0))

    def test_schedule_creation(self):
        self.assertEqual(self.schedule.gym_class, self.exercise)
        self.assertEqual(self.schedule.trainer, self.trainer)
        self.assertEqual(self.schedule.day, date.today())
        self.assertEqual(self.schedule.time, time(hour=10, minute=0))


class EnrollTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser11', password='testtest111')
        self.exercise = Exercise.objects.create(name='exercise1', description='description1test')
        self.enroll = Enroll.objects.create(user=self.user, exercise=self.exercise, date=timezone.now())

    def test_enroll_creation(self):
        self.assertEqual(self.enroll.user, self.user)
        self.assertEqual(self.enroll.exercise, self.exercise)
        self.assertIsNotNone(self.enroll.date)


class HomePageTestCase(TestCase):
    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')


class SignupViewTestCase(TestCase):
    def test_signup_view_with_valid_data(self):
        data = {'username': 'testuser', 'password1': 'testpass', 'password2': 'testpass'}

        response = self.client.post(reverse('signup'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        self.assertEqual(User.objects.count(), 0)

   
