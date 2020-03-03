from django import forms
from django.forms import ModelForm
from challenges.models import Challenge
from containers.models import Container
from teams.models import Team
from users.models import User


class ChallengeForm(ModelForm):

    class Meta:
        model = Challenge
        #fields = '__all__'
        fields = ['title', 'description', 'category', 'points', 'flag', 'hosted', 'imageName', 'ports', 'pathPrefix', 'upload']
        widgets = {
            'title': forms.TextInput(
				attrs={
					'class': 'form-control',
                    'type': 'text'
					}
				),
            'description': forms.Textarea(
				attrs={
					'class': 'form-control',
                    'type': 'text',
                    'rows': '5'
					}
				),
            'category': forms.Select(
				attrs={
					'class': 'form-control'
					}
				),
            'points': forms.NumberInput(
				attrs={
					'class': 'form-control'
					}
				),
            'flag': forms.TextInput(
				attrs={
					'class': 'form-control',
                    'type': 'text'
					}
				),
            'hosted': forms.CheckboxInput(
				attrs={
					# 'class': 'form-check-input',
                    'class': 'custom-control-input',
                    'type': 'checkbox'
					}
				),
            'imageName': forms.TextInput(
				attrs={
					'class': 'form-control',
                    'type': 'text'
					}
				),
            'ports': forms.TextInput(
				attrs={
					'class': 'form-control',
                    'type': 'text'
					}
				),
            'pathPrefix': forms.TextInput(
				attrs={
					'class': 'form-control',
                    'type': 'text'
					}
				),
            'upload': forms.ClearableFileInput(
				attrs={
					'class': 'form-control-file',
                    # 'class': 'custom-file-input',
                    'type': 'file'
					}
				),
			}


class ContainerForm(ModelForm):

    class Meta:
        model = Container
        #fields = '__all__'
        fields = ['name', 'challenge', 'user']
        widgets = {
            'name': forms.TextInput(
				attrs={
					'class': 'form-control',
                    'type': 'text'
					}
				),
            'challenge': forms.Select(
				attrs={
					'class': 'form-control'
					}
				),
            'user': forms.Select(
				attrs={
					'class': 'form-control'
					}
				),
			}


class TeamForm(ModelForm):

    class Meta:
        model = Team
        #fields = '__all__'
        fields = ['name', 'token', 'points', 'hidden', 'correct_flags',  'wrong_flags', 'solved']
        widgets = {
            'name': forms.TextInput(
				attrs={
					'class': 'form-control',
                    'type': 'text'
					}
				),
            'token': forms.TextInput(
				attrs={
					'class': 'form-control',
                    'type': 'text'
					}
				),
            'points': forms.NumberInput(
				attrs={
					'class': 'form-control'
					}
				),
            'hidden': forms.CheckboxInput(
				attrs={
					# 'class': 'form-check-input',
                    'class': 'custom-control-input',
                    'type': 'checkbox'
					}
				),
            'correct_flags': forms.NumberInput(
				attrs={
					'class': 'form-control'
					}
				),
            'wrong_flags': forms.NumberInput(
				attrs={
					'class': 'form-control'
					}
				),
            #TODO: Solved
            }


class UserForm(ModelForm):

    class Meta:
        model = User
        fields = '__all__'
        fields = ['username', 'team', 'hidden']
        widgets = {
            'username': forms.TextInput(
				attrs={
					'class': 'form-control',
                    'type': 'text'
					}
				),
            'team': forms.Select(
				attrs={
					'class': 'form-control'
					}
				),
            'hidden': forms.CheckboxInput(
				attrs={
					# 'class': 'form-check-input',
                    'class': 'custom-control-input',
                    'type': 'checkbox'
					}
				),
            }
    
    

