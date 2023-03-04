import requests
import numpy 
import pandas as pd

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.
def line_notify(request):
    url = "https://api.nasa.gov/planetary/apod"
    api_key = settings.API_KEY
    params = {"api_key": api_key}
    response = requests.get(url, params)
    data = response.json()
    token = settings.LINE_TOKEN
    headers = {"Authorization": "Bearer " + token ,
               "Content-Type" : "application/x-www-form-urlencoded"}
    message = {'message': data['explanation'],
               "imageThumbnail": data['url'], 
               "imageFullsize": data['hdurl']}
    line_response = requests.post("https://notify-api.line.me/api/notify", 
                                  headers=headers, data=message)
    print(line_response.text)
    return HttpResponse(line_response.status_code)


class ListCountryView(APIView):

    def get(self, request, format=None):
        """
        Return a list cities of choosed nation.
        """

        nation = request.GET.get('nation')
        df = pd.read_excel('worldcities.xlsx')
        capital = ['admin', 'primary']
        df_cities_list = df.loc[(df['country'] == nation) & 
                                (df['capital'].isin(capital))]
        cities_list = df_cities_list['admin_name'].unique().tolist()
        random_cities = numpy.random.choice(cities_list, 8)
        return Response(random_cities)


class MapView(TemplateView):
    template_name = "map.html"