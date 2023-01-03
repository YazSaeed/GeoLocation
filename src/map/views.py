from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

from .models import Search
from .forms import SearchForm

import folium
import geocoder

# Create your views here.
def index(request):

    #calling the geocoder
    if request.method  == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = SearchForm()
    if Search.objects.count() != 0:
        address = Search.objects.all().last()
    else:
        address = 'Amman'


    location = geocoder.osm(address)

    latitude = location.lat
    longitude = location.lng
    country = location.country

    if Search.objects.count() == 0 and address == 'Amman':
        map_obj = folium.Map(location = [0, 0], zoom_start=2)

    elif latitude == None or longitude == None:
        address.delete()
        messages.error(request, 'That place doesn\'t exist! Make sure to check the spelling')
        map_obj = folium.Map(location = [0, 0], zoom_start=2)
    else:
        #creating my map object
        map_obj = folium.Map(location = [latitude, longitude], zoom_start=10)
        folium.Marker(location = [latitude,longitude], tooltip='Click for More', popup=country).add_to(map_obj)

    #getting html representation of the map object
    map_obj = map_obj._repr_html_()

    context = {
        'map_obj': map_obj,
        'form':form
    }

    return render(request, 'index.html', context)

