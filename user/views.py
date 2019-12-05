import requests
import csv
import xlsxwriter #write in excel format
import openpyxl
import pandas as pd
from pandas import DataFrame
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.http import HttpResponse
from django.core.mail import send_mail, send_mass_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ClubForm
from member.models import Member
from member.forms import MemberRegisterForm, UpdateMemberForm, UploadFileForm

from .models import Club
try:
    from io import BytesIO as IO # for modern python
except ImportError:
    from io import StringIO as IO # for legacy python

def homepage(request):
    return render(request, 'user/index.html')

def login(request):
    return render(request, 'user/login.html')

def mentions(request):
    """ return the mention page """
    return render(request, 'user/mentions.html')

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
def clubdata(request, club_id):
    club = get_object_or_404(Club, pk=club_id)
    if request.method == 'POST':
        m_form = MemberRegisterForm(request.POST, initial={'club': club_id}) # initial set a default value for 'club' field
        print(m_form)
        if m_form.is_valid():
            new_member = m_form.save(commit=False) # Fill the field 'club' before commit
            new_member.club = club 
            new_member.save()
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
def delete_member(request,club_id, member_id):

    club = get_object_or_404(Club, pk=club_id)
    member = get_object_or_404(Member, pk=member_id)
    Member.objects.get(pk=member_id).delete()
    context = {
        'club':club,
        'member':member,
    }
    return render(request, 'member/delete_member.html', context)

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
    """ Get mails of members who did not provide their document yet and send a reminder """
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
        mail_cm = ('Relance certificat médical', content_mail, 'mickael@sporganizer.herokuapp.com', email_list_cm) # Add email_list_cm
        mail_payment = ('Relance paiement', content_mail, 'mickael@sporganizer.herokuapp.com', email_list_pay) # Add email_list_pay
        send_mass_mail((mail_cm, mail_payment), fail_silently=False)
        context = {
            'club':club,
        }
    return render(request, 'member/mail_sent.html', context)

@login_required
def csv_completed(request, club_id):
    """create csv file and send it to the final user's downloads file"""
    club = get_object_or_404(Club, pk=club_id)
    members = Member.objects.filter(club=club_id)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=membres.csv'

    fieldnames = ['Nom', 'Prénom','Date de naissance', 'Adresse', 'Email', 'Certificat', 'Paiement']
    thewriter = csv.DictWriter(response, fieldnames=fieldnames, delimiter='-')

    thewriter.writeheader()
    for member in members:
        thewriter.writerow({'Nom': member.last_name, 'Prénom': member.first_name, 
        'Date de naissance': member.birth, 'Adresse': member.street_adress, 'Email': member.email, 'Certificat': member.certificate, 'Paiement': member.payment})
    context = {
        'club':club,
    }
    return response

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
    # my "Excel" file, which is an in-memory output file (buffer) 
    excel_file = IO()
    xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter')
    # try to send to user's desktop as a downloaded file
    df.to_excel(xlwriter, sheet_name='sheet1', index=False)
    xlwriter.save()
    xlwriter.close()
    # important step, rewind the buffer or when it is read() you'll get nothing
    # but an error message when you try to open your zero length file in Excel
    excel_file.seek(0)

   # set the mime type so that the browser knows what to do with the file
    response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=membres.xlsx'
    
    return response

@login_required
def upload_xls(request, club_id):
    """ Get an excel file, read and parse datas according to the column attributes"""
    club = get_object_or_404(Club, pk=club_id)
    if request.method == 'POST':
        if not 'myfile' in request.FILES:
            messages.warning(request, f'Aucun fichier chargé !')
        else:
            excel_file = request.FILES['myfile']
            try:
                df = pd.read_excel(excel_file)
                try:
                    for index, row in df.iterrows(): #Read the file row by row with the attribute iterrows()
                        # print(row['Nom'], row['Prénom'], row['Date de naissance'], row['Adresse'], row['Email'], row['Certificat'], row['Paiement']) Check that rows are parsed correctly
                        member = Member.objects.create(
                            last_name = row['Nom'],
                            first_name = row['Prénom'],
                            birth = row['Date de naissance'],           #One row = one member with the column name
                            street_adress = row['Adresse'],
                            email = row['Email'],
                            certificate = row['Certificat'],
                            payment = row['Paiement'],
                            club = club
                        )
                    messages.success(request, f'Fichier importé avec succès !')
                    return redirect('clubdata', club_id)
                except:
                    messages.warning(request, f'Veuillez ajuster les champs: Nom, Prénom, Date de naissance, Adresse, Email, Certificat, Paiement')           
            except:
                messages.warning(request, f'Format Xlsx requis !')
    else:
        messages.warning(request, f'Format Xlsx requis !')
    context = {
        'club':club,
    }
    return render(request, 'member/upload_xls.html', context)
