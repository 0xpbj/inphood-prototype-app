from rest_framework import serializers
from .models import SavedFoodVision

class FoodVisionSerializer(serializers.ModelSerializer):
  class Meta:
    model = SavedFoodVision
