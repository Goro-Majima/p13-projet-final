import requests

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, ClubForm

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
            clubs = Club.objects.filter(owner=request.user)
            if clubs.count() > 0:
                club_list = []
            else:
                club_list = clubs
            context = {
                'club_list':club_list
            }
            return redirect('menu', context)
    else:
        form = ClubForm()
    return render(request, 'user/menu.html', {'form': form})

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
    # return render(request, 'user/register.html')

def results(request):
    message = "results page"
    return HttpResponse(message)

