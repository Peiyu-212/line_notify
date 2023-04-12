import requests
import numpy 
import pandas as pd

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.conf import settings

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response

from .models import City
from .upload import Upload
from .serializer import SelectNationSerializer
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


class ListCountryView(viewsets.GenericViewSet):
    queryset = City.objects.select_related('country').all()
    serializer_class = SelectNationSerializer

    def list(self, request):
        """
        Return a list cities of choosed nation.
        """
        serializer = self.get_serializer(request.query_params)
        cities_list = self.queryset.filter(country__name=serializer.data).values_list(
            'name').distinct()
        random_cities = numpy.random.choice(list(cities_list), 8)
        return Response(random_cities)


class UploadFileViewSet(APIView):

    def post(self, request, format=None):
        upload_file = request.data['file']
        response = Upload(upload_file).upload()
        return Response(response)
    

class MapView(TemplateView):
    template_name = "test.html"