from django import forms

class SubmitClarifai(forms.Form):
  url = forms.URLField()
