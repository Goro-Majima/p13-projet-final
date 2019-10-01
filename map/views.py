from django.shortcuts import render
from django.http import HttpResponse

def homepage(request):
    return render(request, 'map/index.html')

def results(request):
    message = "results page"
    return HttpResponse(message)