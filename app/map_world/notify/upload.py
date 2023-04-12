import pandas as pd
from .models import Country, City
from django.contrib.gis.geos import Point


class Upload:
    def __init__(self, file):
       self.file = pd.read_csv(file)
    
    def upload(self):
        for i in self.file.itertuples():
            id, _ = Country.objects.get_or_create(name=i[4], iso2=i[5], iso3=i[6])
            if i[7] in ['admin', 'primary']:
                City.objects.get_or_create(name=i[0], population=i[9], location=Point(i[3], i[4]),
                                           capital=i[7], country=id)
        return {'status': 'Successful upload!'}