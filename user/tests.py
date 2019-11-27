import datetime
from django.test import TestCase
from django.urls import reverse, resolve
from django.test.client import Client
from user.forms import UserRegisterForm, ClubForm
from django.contrib.auth.models import User
from member.forms import MemberRegisterForm, UpdateMemberForm
from user.models import Club
from django.core.mail import send_mail, send_mass_mail
from django.core import mail

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
class testMassMaill(TestCase):
    """class that test the mass mail function"""
    def setUp(self):
        """ method used to confirm that an email is sent """
        mail_cm = ('Relance certificat médical', 'content_mail', 'lymickael91@gmail.com', ['lyremi89@gmail.com']) 
        mail_payment = ('Relance paiement', 'content_mail2', 'lymickael91@gmail.com', ['lygoku@gmail.com'])
        send_mass_mail((mail_cm, mail_payment), fail_silently=False)

    def test_password_reset_page(self):
            """test that to the Password Reset page that must return HTTP 200 and
            the right template that shows the email form.
            """
            response = self.client.get(reverse('password_reset'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'user/password_reset.html')


    def test_mail_is_sent(self):
        """ Test that messages have been sent. """
        self.assertEqual(len(mail.outbox), 2)

    def test_mail_is_sent_with_the_right_subject(self):
        """ Verify that the subject of the message is correct. """
        self.assertEqual(mail.outbox[0].subject, 'Relance certificat médical')
        self.assertEqual(mail.outbox[1].subject, 'Relance paiement')

    def test_mail_is_sent_to_the_good_person(self):
        """ Verify the destination """
        self.assertEqual(mail.outbox[0].to, ['lyremi89@gmail.com'])
        self.assertEqual(mail.outbox[1].to, ['lygoku@gmail.com'])

# password reset
class TestResetPassword(TestCase):
    """ testing class used to confirm that an email is sent """
    def setUp(self):
        """ method used to confirm that an email is sent """
        mail.send_mail(
            'Réinitialisation du mot de passe sur 127.0.0.1:8000', 'Vous recevez \
            ce message en réponse à votre demande de réinitialisation du mot\
            de passe de votre compte sur 127.0.0.1:8000.',
            'lymickael91@gmail.com', ['user@gmail.com'],
            fail_silently=False,
        )

    def test_password_reset_page(self):
            """test that to the Password Reset page that must return HTTP 200 and
            the right template that shows the email form.
            """
            response = self.client.get(reverse('password_reset'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'user/password_reset.html')


    def test_mail_is_sent(self):
        """ Test that one message has been sent. """
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['user@gmail.com'])

    def test_mail_is_sent_with_the_right_subject(self):
        """ Verify that the subject of the message is correct. """
        self.assertEqual(mail.outbox[0].subject, 'Réinitialisation du mot de passe sur 127.0.0.1:8000')

    def test_mail_is_sent_with_right_email(self):
        """ Check that a mail the user is redirected after recognized email"""
        response = self.client.post(reverse('password_reset'), {'email':'lymickael91@gmail.com'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/password-reset/done')

    def test_password_is_reset(self):
        """ check that the new password page is ok """
        response = self.client.post(reverse('password_reset_confirm', args={'uidb64':'MTA', 'token':'5af-f27d40734f5bc8ba3c9a'}))
        self.assertEqual(response.status_code, 200)
        response2 = self.client.post(reverse('password_reset_confirm', args={'uidb64':'MTA', 'token':'5af-f27d40734f5bc8ba3c9a'}), data={'new_password1':'Testing321', 'new_password2':'Testing321'})
        self.assertEqual(response2.status_code, 200)

    def test_password_not_complete(self):
        """ check result when password is incomplete """
        response = self.client.post(reverse('password_reset_confirm', args={'uidb64':'MTA', 'token':'5af-f27d40734f5bc8ba3c9a'}), data={'new_password1':'Testing321', 'new_password2':'Abdcdfdfd321'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user/password_reset_confirm.html')
