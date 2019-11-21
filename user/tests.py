import datetime
from django.test import TestCase
from django.urls import reverse, resolve
from django.test.client import Client
from user.forms import UserRegisterForm, ClubForm
from django.contrib.auth.models import User
from member.forms import MemberRegisterForm, UpdateMemberForm
from user.models import Club
# Homepage
class IndexPageTestCase(TestCase):
    """ Class Test that the function returns the home page with response 200 """
    def test_index_page(self):
        """ Test that the function returns the home page with response 200 """
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)

# Registration
class RegisterPageTestCase(TestCase):
    """ Class test that the function returns to the home page after registration"""
    def setUp(self):
        self.client = Client()

    def test_register_page(self):
        """ check the form """
        form_data = {'username':'john',
                     "email":'lennon@thebeatles.com',
                     "password1":'Abracadabra0',
                     'password2':'Abracadabra0'}
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())
        response = self.client.post(reverse('register'), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_user_already_exists(self):
        self.user = User.objects.create_user('jacob', 'test123')
        data = {
            'username': 'jacob',
            'password1': 'test123',
            'password2': 'test123',
        }
        form = UserRegisterForm(data)
        self.assertFalse(form.is_valid())

    def test_not_register_page(self):
        """ check the response status code with a password pretty similar with the username"""
        self.user = User.objects.create_user('vic', 'vicpassword')
        self.client.login(password='johnpassword')
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

# Login
class LoginTestCase(TestCase):
    """ Class make sure the user is redirected to the homepage after login """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    def test_Login(self):
        """ check status code """
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('menu'))
        self.assertEqual(response.status_code, 200)

    def test_login_fails(self):
        self.client.login(username='john', password='john')
        response = self.client.get(reverse('menu'))
        self.assertEqual(response.status_code, 302)

# Creation of a club
class ClubCreationTestCase(TestCase):
    """ Class that check that a club is created and displayed only to its owner"""
    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        
    def test_add_club(self):
        form_data = {
            "club_name":"Kbm",
            "zip_code":"77144",
            "city":"Paris"
        }
        form = ClubForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_club_fails(self):
        """ try to create with an empty field """
        form_data = {
            "club_name":"Kbm",
            "zip_code":"",
            "city":"Paris"
        }
        form = ClubForm(data=form_data)
        self.assertFalse(form.is_valid())

# Creation of a member
class CreationMemberTestCase(TestCase):
    """Class that check that a member is created and displayed only to its owner""" 
    def setUp(self):
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')
        self.club = Club.objects.create(club_name='KBM', zip_code='77144', city='evry', owner= self.user)
    
    def test_member_is_created(self):
        form_data = {
            "last_name":"Benzema",
            "first_name": "Karim",
            "birth": datetime.date(1956,1,30),
            "street_adress": '3 rue du veau',
            "email": 'benzema@gmail.com',
            "certificate": True,
            "payment": False,
            "club": self.club
        }
        form = MemberRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_member_is_not_created(self):
        form_data = {
            "last_name":"Benzema",
            "first_name": "Karim",
            "birth": datetime.date(1956,1,30),
            "street_adress": '3 rue du veau',
            "email": 'bom',
            "certificate": True,
            "payment": False,
            "club": self.club
        }
        form = MemberRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_page_clubdata_is_returned(self):
        form = MemberRegisterForm()
        form.is_valid = True
        response = self.client.post(reverse('clubdata', args=(self.club.id,)))
        self.assertEqual(response.status_code, 200)

    def test_view_returns_clubdata_page(self):
        response = self.client.post(reverse('clubdata', args=(self.club.id,)))
        self.assertTemplateUsed(response, 'member/clubdata.html')

    def test_page_clubdata_returns_404(self):
        response = self.client.post(reverse('clubdata', args=(150,)))
        self.assertEqual(response.status_code, 404)

# Edition of member datas

# Dump of the database into an excel file

# mail function
    
      

