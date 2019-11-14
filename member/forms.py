from django import forms
from member.models import Member

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
                'email', 'certificate', 'payment', 'club'
                ]

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