from django import forms

class SubmitFoodVision(forms.Form):
  url = forms.URLField()
