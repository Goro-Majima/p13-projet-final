# -*- coding: utf-8 -*-
import requests
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        url = "https://webcamstravel.p.rapidapi.com/webcams/list/country=vn"

        querystring = {"lang":"en","show":"webcams:image,location"}

        headers = {
            'x-rapidapi-host': "webcamstravel.p.rapidapi.com",
            'x-rapidapi-key': "d72fcdc567msh584958394514d56p11eb8fjsn7f19d7e4aeb9"
            }

        response = requests.request("GET", url, headers=headers, params=querystring)

        print(response.text)