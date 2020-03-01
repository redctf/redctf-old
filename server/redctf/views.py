from django.conf import settings
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.decorators import user_passes_test

from users.models import User
from challenges.models import Challenge
from containers.models import Container
from teams.models import Team
from users.models import User
from .forms import ChallengeForm
from .forms import ContainerForm
from .forms import TeamForm
from .forms import UserForm


#     #  TODO  - lock down view to only super users
#     #  TODO  - replicate admin thru templating engine or raw JS/HTML
#     #  TODO  - update traefik to route accordingly
#     #  TODO  - Stretch goal, return non-super user template to discourage further tampering

@xframe_options_exempt
#@user_passes_test(lambda u: u.is_superuser)
def admin_panel(request):

    if request.user.is_superuser:
        return render(request, 'admin.html')
    else:
        return render(request, 'ahahah.html')



################ challenges ################
@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def challenge_list(request):
    challenges = Challenge.objects.all().order_by('created')
    return render(request, 'challenge_list.html', {'challenges' : challenges})

@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def challenge_detail(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk)
    return render(request, 'challenge_detail.html', {'challenge': challenge})

@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def challenge_new (request):

    if request.method == 'POST':
        form = ChallengeForm(request.POST)
        if form.is_valid():
            new_challenge = form.save()

            return redirect('challenge_detail', pk=new_challenge.pk)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ChallengeForm()

    return render(request, 'challenge_edit.html', {'form': form})

@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def challenge_edit(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk)
    if request.method == "POST":
        form = ChallengeForm(request.POST, instance=challenge)
        # check whether it's valid:
        if form.is_valid():
            # save the for to the db
            new_challenge = form.save()

            # redirect to challenge detail page
            return redirect('challenge_detail', pk=new_challenge.pk)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ChallengeForm(instance=challenge)

    return render(request, 'challenge_edit.html', {'form': form})
############################################

################ containers ################
@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def container_list(request):
    containers = Container.objects.all().order_by('created')
    return render(request, 'container_list.html', {'containers' : containers})

############################################

################## teams ###################
@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def team_list(request):
    teams = Team.objects.all().order_by('created')
    return render(request, 'team_list.html', {'teams' : teams})

############################################

################## users ###################
@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def user_list(request):
    users = User.objects.all().order_by('created')
    return render(request, 'user_list.html', {'users' : users})

############################################