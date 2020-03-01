from django.forms import ModelForm
from challenges.models import Challenge
from containers.models import Container
from teams.models import Team
from users.models import User


class ChallengeForm(ModelForm):

    class Meta:
        model = Challenge
        fields = '__all__'


class ContainerForm(ModelForm):

    class Meta:
        model = Container
        fields = '__all__'


class TeamForm(ModelForm):

    class Meta:
        model = Team
        fields = '__all__'


class UserForm(ModelForm):

    class Meta:
        model = User
        fields = '__all__'
    
    

