from django.shortcuts import render
from django.conf import settings
import requests
import json
import os
import io
import xml.etree.ElementTree as ET

# Create your views here.

from .forms import SubmitClarifai
from .serializer import ClarifaiSerializer

def save_clarifai(request):
  if request.method == "POST":
    form = SubmitClarifai(request.POST)
    if form.is_valid():
      payload = {"grant_type":"client_credentials", "client_id":settings.CLARIFAI_CLIENT_ID, "client_secret":settings.CLARIFAI_CLIENT_SECRET}
      t = requests.post('https://api.clarifai.com/v1/token/', data=payload)
      url = form.cleaned_data['url']
      headers = {'Authorization':'Bearer {}'.format(t.json()['access_token'])}
      r = requests.get('https://api.clarifai.com/v1/tag/?url=' + url, headers=headers)
      guesses = set(r.json()['results'][0]['result']['tag']['classes'])
      print(guesses)
      #probs = r.json()['results'][0]['result']['tag']['probs']
      #print(probs)
      fruits = []
      fruitsFile = os.path.join(settings.BASE_DIR, 'fruits.txt')
      fruits = [line.rstrip('\n') for line in open(fruitsFile)]
      fruitsFound = [val for val in fruits if val.lower() in guesses]
      #print (fruitsFound)
      vegetables = []
      vegetablesFile = os.path.join(settings.BASE_DIR, 'vegetables.txt')
      vegetables = [line.rstrip('\n') for line in open(vegetablesFile)]
      vegetablesFound = [val for val in vegetables if val.lower() in guesses]
      #print (vegetablesFound)
      fruitIds = []
      vegetableIds = []
      for x in fruitsFound:
        x += ", raw"
        usda_headers = {"Content-Type":"application/json"}
        usda_data = {"q":x,"max":"5","offset":"0","group":"Fruits and Fruit Juices",}
        fr = requests.get('http://api.nal.usda.gov/ndb/search/?api_key=' + settings.USDA_API_KEY, usda_data, headers=usda_headers)
        #print(fr.url)
        #print (fr.json())
        fruitIds.append(fr.json()['list']['item'][0]['ndbno'])
      for x in vegetablesFound:
        x += ", raw"
        usda_headers = {"Content-Type":"application/json"}
        usda_data = {"q":x,"max":"5","offset":"0","group":"Vegetables and Vegetable Products",}
        fr = requests.get('http://api.nal.usda.gov/ndb/search/?api_key=' + settings.USDA_API_KEY, usda_data, headers=usda_headers)
        #print(fr.url)
        #print (fr.json())
        vegetableIds.append(fr.json()['list']['item'][0]['ndbno'])
      
      for x in fruitIds:
        usda_headers = {"Content-Type":"application/json"}
        usda_data = {"ndbno":x}
        fr = requests.get('http://api.nal.usda.gov/ndb/reports/?api_key=' + settings.USDA_API_KEY, usda_data, headers=usda_headers)
        print(fr.json())
      
      for x in vegetableIds:
        usda_headers = {"Content-Type":"application/json"}
        usda_data = {"ndbno":x}
        fr = requests.get('http://api.nal.usda.gov/ndb/reports/?api_key=' + settings.USDA_API_KEY, usda_data, headers=usda_headers)
        print(fr.json())

  else:
    form = SubmitClarifai()
  return render(request, 'index.html', {'form': form})
