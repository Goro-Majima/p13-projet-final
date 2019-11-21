import requests
import csv
from pandas import DataFrame
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.mail import send_mail, send_mass_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ClubForm
from member.models import Member
from member.forms import MemberRegisterForm, UpdateMemberForm

from .models import Club

def homepage(request):
    return render(request, 'user/index.html')

def login(request):
    return render(request, 'user/login.html')

@login_required
def menu(request):
    if request.method == 'POST':
        form = ClubForm(request.POST)
        if form.is_valid():
            club = form.save(commit=False)
            club.owner = request.user
            club.save()
            name = form.cleaned_data.get('club_name')
            messages.success(request, f'Le club {name} est ajouté.')
            return redirect('menu')
    else:
        form = ClubForm()
    clubs = Club.objects.filter(owner=request.user)
    if clubs.count() == 0:
        club_list = []
    else:
        club_list = clubs
    context = {
        'club_list': club_list,
        'form': form
    }
    return render(request, 'user/menu.html', context)

def register(request):
    """ Check if the form is valid, create a user and save it to the database """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'votre compte est créé {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form':form})

@login_required
def clubhomepage(request):
    return render(request, 'user/clubhomepage.html')

@login_required
def clubdata(request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    if request.method == 'POST':
        m_form = MemberRegisterForm(request.POST, initial={'club': club_id}) # initial set a default value for 'club' field
        print(m_form)
        if m_form.is_valid():
            m_form.save()
            messages.success(request, f'Un membre a été créé !')
            m_form = MemberRegisterForm()
    else:
        m_form = MemberRegisterForm(initial={'club': club_id})
    members = Member.objects.filter(club=club_id)
    context = {
        'club':club,
        'm_form': m_form,
        'members': members,
    }
    return render(request, 'member/clubdata.html', context)

@login_required
def editpage(request,club_id, member_id):
    club = get_object_or_404(Club, pk=club_id)
    member = get_object_or_404(Member, pk=member_id)
    if request.method == 'POST':
        u_form = UpdateMemberForm(request.POST, instance=member)
        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Membre mis à jour !')
            return redirect('clubdata', club_id)
    else:
        u_form = UpdateMemberForm(instance=member)
    context = {
        'club':club,
        'member':member,
        'u_form': u_form,
    }
    return render(request, 'member/editpage.html', context)

@login_required
def certificate_recall(request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    list_members_without_certificate=[]
    list_members_without_payment=[]
    members_without_certificate = Member.objects.filter(club=club_id, certificate=False)
    members_without_payment = Member.objects.filter(club=club_id, payment=False)
    list_members_without_certificate = members_without_certificate
    list_members_without_payment = members_without_payment
    context = {
        'club':club,
        'list_members_without_certificate':list_members_without_certificate,
        'list_members_without_payment':list_members_without_payment,
    }
    return render(request, 'member/certificate_recall.html', context)

@login_required
def mail_sent(request, club_id):
    if request.method == 'GET':
        content_mail = request.GET.get('message')
        club = get_object_or_404(Club, pk=club_id)
        list_members_without_certificate=[]
        list_members_without_payment=[]
        members_without_certificate = Member.objects.filter(club=club_id, certificate=False)
        members_without_payment = Member.objects.filter(club=club_id, payment=False)
        list_members_without_certificate = members_without_certificate
        list_members_without_payment = members_without_payment
        email_list_cm = []
        email_list_pay = []
        for member in list_members_without_certificate:
            email_list_cm.append(member.email)
        for member in list_members_without_payment:
            email_list_pay.append(member.email)
        # for member_pay in list_members_without_payment:
        #     if member_pay.email not in email_list_cm:
        #         email_list_pay.append(member_pay.email)
        
        mail_cm = ('Relance certificat médical', content_mail, 'lymickael91@gmail.com', ['lyremi89@gmail.com']) # Add email_list_cm
        mail_payment = ('Relance paiement', content_mail, 'lymickael91@gmail.com', ['lyremi89@gmail.com']) # Add email_list_pay
        send_mass_mail((mail_cm, mail_payment), fail_silently=False)
        context = {
            'club':club,
        }
    return render(request, 'member/mail_sent.html', context)

# @login_required
# def csv_completed(request, club_id):
#     club = get_object_or_404(Club, pk=club_id)
#     members = Member.objects.filter(club=club_id)
#     with open('données_membres.csv', 'w', newline='') as f:
#         fieldnames = ['Nom', 'Prénom','Date de naissance', 'Adresse', 'Email', 'Certificat', 'Paiement']
#         thewriter = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')

#         thewriter.writeheader()
#         for member in members:
#             thewriter.writerow({'Nom': member.last_name, 'Prénom': member.first_name, 
#             'Date de naissance': member.birth, 'Adresse': member.street_adress, 'Email': member.email, 'Certificat': member.certificate, 'Paiement': member.payment})
#     context = {
#         'club':club,
#     }
#     return render(request, 'member/csv_completed.html', context)

@login_required
def xls_completed(request, club_id):
    """ create an excel file and send it to the final user's downloads file"""
    club = get_object_or_404(Club, pk=club_id)
    members = Member.objects.filter(club=club_id)
    l_last_names = []
    l_first_names = []
    l_birth = []
    l_street_adress = []
    l_email = []
    l_certificate = []
    l_payment = []
    for member in members:
        l_last_names.append(member.last_name)
        l_first_names.append(member.first_name)
        l_birth.append(member.birth)
        l_street_adress.append(member.street_adress)
        l_email.append(member.email)
        l_certificate.append(member.certificate)
        l_payment.append(member.payment)
    df = DataFrame({
        'Nom': l_last_names, 
        'Prénom': l_first_names, 
        'Date de naissance': l_birth, 
        'Adresse': l_street_adress,
        'Email':l_email,
        'Certificat': l_certificate,
        'Paiement': l_payment
        })
    # try to send to user's desktop as a downloaded file
    df.to_excel('C:/Users/Alex Tour/Desktop/PYTHON/projet openclassrooms/Projet13/données_club.xlsx', sheet_name='sheet1', index=False)
    context = {
        'club':club,
    }
    return render(request, 'member/xls_completed.html', context)