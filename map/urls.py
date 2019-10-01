from django.conf.urls import url
from django.urls import path

from . import views # import views so we can use them in urls.


urlpatterns = [
    path('', views.homepage), 
    path('results', views.results)
]