""" Python file importing and create a form for a user registration """
from django import forms
from django.contrib.auth.models import User
from member.models import Member
from django.contrib.auth.forms import UserCreationForm
from .models import Club

class UserRegisterForm(UserCreationForm):
    """ Use django UserCreationForm which is an app form for a registration """
    email = forms.EmailField()

    class Meta:
        model = User
        labels = {
            'username':'Identifiant',
            'password1':'Mot de passe'
        }
        fields = ['username', 'email', 'password1', 'password2']

class ClubForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(ClubForm, self).clean()
        name = cleaned_data.get('club_name')
        zip_code = cleaned_data.get('zip_code')
        city = cleaned_data.get('city')
        if not name and not zip_code and not city:
            raise forms.ValidationError('Vous devez compléter tous les champs')
    
    class Meta:
        model = Club
        labels = {
            'club_name':'Club',
            'zip_code':'Code postal',
            'city':'Ville'
        }
        fields = ['club_name', 'zip_code', 'city']
