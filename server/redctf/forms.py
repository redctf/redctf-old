from django import forms

class CreateChallenge(forms.Form):
    title = forms.CharField(max_length=100)
    description = forms.CharField(max_length=512)
    points = forms.IntegerField()
    flag = forms.CharField(max_length=100)
    hosted = forms.BooleanField()
    imageName = forms.CharField(max_length=100)
    ports = forms.CharField(max_length=100)
    pathPrefix = forms.CharField(max_length=100)
    upload = forms.FileField()

