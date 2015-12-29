from rest_framework import serializers
from .models import SavedClarifai

class ClarifaiSerializer(serializers.ModelSerializer):
  class Meta:
    model = SavedClarifai
