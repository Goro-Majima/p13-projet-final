import requests
from django import forms
from member.models import Member
from user.models import Club

class MemberRegisterForm(forms.ModelForm):


    class Meta:
        model = Member
        labels = {
            'last_name':'Nom',
            'first_name':'Prénom',
            'birth':'Date de naissance',
            'street_adress':'Adresse',
            'certificate':'Certificat médical',
            'payment':'Paiement'
        }
        fields = ['last_name', 'first_name', 'birth', 'street_adress', 
                'email', 'certificate', 'payment'
                ]
                
    # """ disable the field club in order to prevent other input"""
    # def __init__(self, *args, **kwargs):
    #     super(MemberRegisterForm, self).__init__(*args, **kwargs)
    #     self.fields['club'].disabled = False

class UpdateMemberForm(forms.ModelForm):

    class Meta:
        model = Member
        labels = {
            'last_name':'Nom',
            'first_name':'Prénom',
            'birth':'Date de naissance',
            'street_adress':'Adresse',
            'certificate':'Certificat médical',
            'payment':'Paiement'
        }
        fields = ['last_name', 'first_name', 'birth', 'street_adress', 
                'email', 'certificate', 'payment'
                ]