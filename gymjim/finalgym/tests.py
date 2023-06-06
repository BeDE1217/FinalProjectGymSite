from django.test import TestCase
from django.urls import reverse
from .models import News, Schedule, Exercise, Trainer, Enroll,  Price
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

   
class LoginViewTestCase(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpass'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_login_with_valid_credentials(self):
        data = {'username': self.username, 'password': self.password}

        response = self.client.post(reverse('login'), data)
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_with_invalid_credentials(self):
        data = {'username': self.username, 'password': 'incorrect'}

        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, 'Invalid username or password!')
        self.assertFalse(response.wsgi_request.user.is_authenticated)


class ContactViewTestCase(TestCase):
    def test_contact_view_with_valid_data(self):
        data = {
            'email': 'test@example.com',
            'phone': '123456789',
            'topic': 'Test Topic',
            'message': 'Test Message'
        }

        response = self.client.post(reverse('contact_view'), data)
        self.assertTemplateUsed(response, 'contact success.html')

    def test_contact_view_with_invalid_data(self):
        data = {
            'email': '',
            'phone': '',
            'topic': '',
            'message': ''
        }

        response = self.client.post(reverse('contact_view'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact success.html')


class UserProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_user_profile(self):
        response = self.client.get(reverse('user_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_profile.html')


class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_logout_view(self):
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('home'))
        self.assertFalse('_auth_user_id' in self.client.session)


class PricesListViewTestCase(TestCase):
    def setUp(self):
        Price.objects.create(name='Price 1', amount=10)
        Price.objects.create(name='Price 2', amount=20)
    def test_priceslist_view(self):
        response = self.client.get(reverse('priceslist'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'prices.html')
        self.assertContains(response, 'Price 1')
        self.assertContains(response, 'Price 2')


class TrainersViewTestCase(TestCase):
    def setUp(self):
        Trainer.objects.create(name='Trainer1', bio='biotest1')

    def test_trainerslist_view(self):
        response = self.client.get(reverse('trainerslist'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'trainers.html')
        self.assertContains(response, 'Trainer1')
        self.assertContains(response, 'biotest1')
