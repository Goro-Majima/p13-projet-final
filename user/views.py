import requests

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ClubForm, MemberRegisterForm
# from member.forms import MemberRegisterForm

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
        m_form = MemberRegisterForm(request.POST)
        if m_form.is_valid():
            m_form.save()
            messages.success(request, f'Un membre a été créé !')
    else:
        m_form = MemberRegisterForm()
    context = {
        'club':club,
        'm_form': m_form,
    }
    return render(request, 'member/clubdata.html', context)