from django.conf import settings
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.decorators import user_passes_test

from django.db.models import Count

from users.models import User
from challenges.models import Challenge
from containers.models import Container
from teams.models import SolvedChallenge
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
    return render(request, 'challenges/challenge_list.html', {'challenges' : challenges})

@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def challenge_detail(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk)
    return render(request, 'challenges/challenge_detail.html', {'challenge': challenge})

@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def challenge_delete(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk)
    challenge.delete()
    return redirect(challenge_list)

@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def challenge_new (request):

    if request.method == 'POST':
        form = ChallengeForm(request.POST)
        if form.is_valid():
            new_challenge = form.save()

            return redirect('challenges/challenge_detail', pk=new_challenge.pk)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ChallengeForm()

    return render(request, 'challenges/challenge_edit.html', {'form': form})

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
            return redirect('challenges/challenge_detail', pk=new_challenge.pk)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ChallengeForm(instance=challenge)

    return render(request, 'challenges/challenge_edit.html', {'form': form})
############################################

################ containers ################
@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def container_list(request):
    containers = Container.objects.all().order_by('created')
    return render(request, 'containers/container_list.html', {'containers' : containers})

@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def container_detail(request, pk):
    container = get_object_or_404(Container, pk=pk)
    return render(request, 'containers/container_detail.html', {'container': container})

@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def container_delete(request, pk):
    container = get_object_or_404(Container, pk=pk)
    container.delete()
    return redirect(container_list)

@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def container_new (request):

    if request.method == 'POST':
        form = ContainerForm(request.POST)
        if form.is_valid():
            new_container = form.save()

            return redirect('container_detail', pk=new_container.pk)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ContainerForm()

    return render(request, 'containers/container_edit.html', {'form': form})

@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def container_edit(request, pk):
    container = get_object_or_404(Container, pk=pk)
    if request.method == "POST":
        form = ContainerForm(request.POST, instance=container)
        # check whether it's valid:
        if form.is_valid():
            # save the for to the db
            new_container = form.save()

            # redirect to container detail page
            return redirect('container_detail', pk=new_container.pk)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ContainerForm(instance=container)

    return render(request, 'containers/container_edit.html', {'form': form})
############################################

################## teams ###################
@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def team_list(request):
    teams = Team.objects.all().order_by('created')
    return render(request, 'teams/team_list.html', {'teams' : teams})

@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    return render(request, 'teams/team_detail.html', {'team': team})

@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def team_delete(request, pk):
    team = get_object_or_404(Team, pk=pk)
    team.delete()
    return redirect(team_list)

@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def team_new (request):

    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            new_team = form.save()

            return redirect('team_detail', pk=new_team.pk)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TeamForm()

    return render(request, 'teams/team_edit.html', {'form': form})

@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def team_edit(request, pk):
    team = get_object_or_404(Team, pk=pk)
    if request.method == "POST":
        form = TeamForm(request.POST, instance=team)
        # check whether it's valid:
        if form.is_valid():
            # save the for to the db
            new_team = form.save()

            # redirect to team detail page
            return redirect('team_detail', pk=new_team.pk)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TeamForm(instance=team)

    return render(request, 'teams/team_edit.html', {'form': form})

############################################

################## users ###################
@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def user_list(request):
    users = User.objects.all().order_by('created')
    return render(request, 'users/user_list.html', {'users' : users})

@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'users/user_detail.html', {'user': user})

@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return redirect(user_list)

@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def user_new (request):

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = form.save()

            return redirect('user_detail', pk=new_user.pk)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UserForm()

    return render(request, 'users/user_edit.html', {'form': form})

@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        # check whether it's valid:
        if form.is_valid():
            # save the for to the db
            new_user = form.save()

            # redirect to user detail page
            return redirect('user_detail', pk=new_user.pk)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UserForm(instance=user)

    return render(request, 'users/user_edit.html', {'form': form})

############################################