# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from signup.models import CityDetails
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse, HttpResponseRedirect
import json
from jsonview.decorators import json_view
from django.template.loader import render_to_string




def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup/signup.html', {'form': form})

@json_view
@csrf_protect
def city_api(request):
    if request.method == 'GET':
	resp = request.GET['data']
	location , state , lat, longi = resp.split("___")
	city = CityDetails.objects.create(user = request.user, location = location, state = state, latitude = lat, longitude = longi)
	row_html = render_to_string('signup/row.html', {"status":2, 'location':location,'state':state, 'lat':lat, 'long':longi})
	print row_html
	return {'success':True, 'row': row_html}

	
		
@json_view
@csrf_protect	  
def get_city_detail(request):
    import requests
    if request.method == 'GET':
        address = request.GET['city']
#        api_key = "AIzaSyDyJvq_Q5uhbVmMa32S1J8RVhz-ikHjACI"
#        api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(address, api_key))
        api_response =  requests.get('https://maps.googleapis.com/maps/api/geocode/json?&address={0}'.format(address))
        api_response_dict = api_response.json()
        if api_response_dict["status"] == "OK":
	    resp = api_response_dict["results"]
	    for i in resp:
		state = i["formatted_address"]
	    for j in resp:
	        lat = j["geometry"]["location"]["lat"]
	        longi = j["geometry"]["location"]["lng"]
	    row_html = render_to_string('signup/row.html', {"status":1, "location":address,"state":state, "lat": lat , "long": longi})
	    return {"success":True , 'row':row_html}
	else:
	    return {"success":False, "msg":"ENTERED CITY NOT FOUND"}
	   
    else:
	return HttpResponse("NOT A VALID REQUEST") 

@json_view
@csrf_protect
def user_selected_data(request):
    if request.method == "GET":
	user = request.user
	city = CityDetails.objects.filter(user = user).order_by('-id')
	row_html = render_to_string('signup/row.html',{"status":3,"city":city})
	print row_html
	return {'success':True, 'row':row_html}			
