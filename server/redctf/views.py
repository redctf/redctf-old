from django.conf import settings
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.clickjacking import xframe_options_exempt
from django.contrib.auth.decorators import user_passes_test

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from django.db.models import Count

from users.models import User
from challenges.models import Challenge
from categories.models import Category
from containers.models import Container
from ctfs.models import Ctf
from teams.models import SolvedChallenge
from teams.models import Team
from users.models import User
from .forms import CategoryForm
from .forms import ChallengeForm
from .forms import ContainerForm
from .forms import CtfForm
from .forms import TeamForm
from .forms import UserForm

import re
from dockerAPI.dockerAPI import *
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError
from redctf.settings import RDB_HOST, RDB_PORT, CTF_DB
import uuid
from django.utils.dateformat import format


d = dockerAPI()

#     #  TODO  - update traefik to route accordingly
#     #  TODO  - handle exceptions (ex: dockerfile doesn't build)
#     #  TODO  - update or delete solved challenges on team model as well as a good way to create/edit/delete solved challenges
#     #  TODO  - add team token generation to resetdb.py
#     #  TODO  - don't push token to rethink by implementing get token query to only return your team's token
#     #  TODO  - user password set for add and edit user
#     #  TODO  - when deleting category it doesn't disappear from challenge board


@xframe_options_exempt
#@user_passes_test(lambda u: u.is_superuser)
def admin_panel(request):

    if request.user.is_superuser:
        return render(request, 'adminpanel.html')
    else:
        return render(request, 'ahahah.html')


################## categories ###################
@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def category_list(request):
    categories = Category.objects.all().order_by('created')
    return render(request, 'adminpanel/categories/category_list.html', {'categories' : categories})

@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return render(request, 'adminpanel/categories/category_detail.html', {'category': category})

@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)

    #try rethink delete, then django delete
    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    try:
        r.db(CTF_DB).table('categories').filter({'sid':category.id}).delete().run(connection)
        category.delete()
    except Exception as e:
        #raise Exception('Error deleting category from realtime database: %s' % (e))
        print('Error deleting category: %s' % (e))
    finally:
        connection.close()

    return redirect(category_list)

@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def category_new (request):

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():

            #create category object so we have id
            new_category = form.save()

            # Push category to rethinkdb database
            connection = r.connect(host=RDB_HOST, port=RDB_PORT)
            try:
                r.db(CTF_DB).table('categories').insert({ 'sid': new_category.id, 'name': new_category.name, 'created': format(new_category.created, 'U')}).run(connection)
            except Exception as e:
                raise Exception('Error adding category: %s' % (e))
            finally:
                connection.close()


            return redirect('category_detail', pk=new_category.pk)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CategoryForm()

    return render(request, 'adminpanel/categories/category_edit.html', {'form': form})

@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        # check whether it's valid:
        if form.is_valid():

            if form.has_changed():

                # save category object
                new_category = form.save()

                rethink_updates = {}

                for i in form.changed_data:
                    rethink_updates[i] = form.cleaned_data[i]

                print(rethink_updates)

                connection = r.connect(host=RDB_HOST, port=RDB_PORT)
                if len(rethink_updates) != 0:
                    try:
                        r.db(CTF_DB).table('categories').filter( {'sid': new_category.id} ).update(rethink_updates).run(connection)
                    except RqlRuntimeError as e:
                        #raise Exception('Error updating category from realtime database: %s' % (e))
                        print('Error updating category from realtime database: %s' % (e))
                    finally:
                        connection.close()
        
            # redirect to category detail page
            return redirect('category_detail', pk=new_category.pk)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CategoryForm(instance=category)

    return render(request, 'adminpanel/categories/category_edit.html', {'form': form})

############################################

################ challenges ################
@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def challenge_list(request):
    challenges = Challenge.objects.all().order_by('created')
    return render(request, 'adminpanel/challenges/challenge_list.html', {'challenges' : challenges})

@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def challenge_detail(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk)
    return render(request, 'adminpanel/challenges/challenge_detail.html', {'challenge': challenge})

@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def challenge_delete(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk)


    connection = r.connect(host=RDB_HOST, port=RDB_PORT)

    teams = getDjangoTeamsWithSolvedChallengesByID(challenge.id)
    
    rethink_updates = {}
    if teams:
        # print('matching teams')
        try:
            for team in teams: 
                print('Updating {0}\'s points.'.format(team.name))  
                            
                # calculate the difference in points from old points value to new.
                    
                rethink_teams = r.db(CTF_DB).table('teams').filter({'sid':team.id}).run(connection)    
                    
                # use for loop to access the object(s) values and assign to team id variable
                for rethink_team in rethink_teams: 
                    print(rethink_team['id'])   
                    rethink_team_id = rethink_team['id']
                    
                rethink_team_object = r.db('redctf').table(
                'teams').get(rethink_team_id).run(connection)
                    
                # get rethink team solved object 
                solved_object = rethink_team_object['solved']

                # set django team points
                team.points -= challenge.points
                    
                # set django correct_flags
                team.correct_flags -= 1 
                                    
                # save backend updated team points
                team.save()
                    
                # set update for rethinkdb team points
                rethink_updates['points'] = team.points
                    
                # set update for rethinkdb team correct flags
                rethink_updates['correct_flags'] = team.correct_flags
                    
                # remove solved challenge object
                solved_challenge = team.solved.get(challenge_id=challenge.id)
                    
                    
                rethink_updated_solved_object = []
                # find solved challenges to delete within rethink solved object
                # this will update the solved challenges to be everything except the one being deleted. 
                for index, rethink_solved_chall in enumerate(solved_object):
                    if rethink_solved_chall['id'] != challenge.id:
                        rethink_updated_solved_object.append(rethink_solved_chall)
                    
                # update solved object for rethink update (with challenge removedt)
                rethink_updates['solved'] = rethink_updated_solved_object
                    
                # run updates on rethink
                update = r.db('redctf').table('teams') \
                    .get(rethink_team_id)\
                    .update(rethink_updates).run(connection)
                print('updates: {0}'.format(update))
                    
                # delete rethink solved challenge
                solved_challenge.delete()
                    
        except Exception as ex:
            #raise Exception('error with teams: {0}'.format(ex))
            print('error with teams: {0}'.format(ex))
        
    else:
        print('no matching teams')


    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    try:
        r.db(CTF_DB).table('challenges').filter({'sid':challenge.id}).delete().run(connection)
        challenge.delete()
    except Exception as e:
        #raise Exception('Error deleting challenge from realtime database: %s' % (e))
        print('Error deleting challenge: %s' % (e))
    finally:
        connection.close()

    return redirect(challenge_list)

@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def challenge_new (request):

    if request.method == 'POST':
        form = ChallengeForm(request.POST, request.FILES)
        if form.is_valid():
            #No validation here (should already be done .is_valid)
            
            #need to save to assign id
            new_challenge = form.save()

            #parse dockerfile for list of ports
            if new_challenge.upload:
                if new_challenge.hosted:
                    
                    try:
                        ports = list()
                        for line in new_challenge.upload.file:
                            line = line.decode('utf-8')
                            start = 'EXPOSE '

                            if (start in line):
                                possible_port = (line[line.find(start)+len(start):])
                                ports.append(possible_port.split())

                        # flatten list
                        flattened_ports = list(set([val for sublist in ports for val in sublist]))
                        print (flattened_ports)

                        if len(flattened_ports):
                            new_challenge.ports = flattened_ports
                        else:
                            new_challenge.ports = '****no exposed ports****'

                    except Exception as e:
                        #raise Exception('Error parsing uploaded Dockerfile: ', e)
                        print ('Error parsing uploaded Dockerfile: ', e)
                        new_challenge.ports = '****error parsing ports****'
                    
            #set var for pathPrefix and tag
            #path_tag = str(new_challenge.id) + '_' + re.sub('[^A-Za-z0-9]+', '', new_challenge.category.name.lower()) + str(new_challenge.points)
            path_tag = 'chall_' + str(new_challenge.id)
            new_challenge.pathPrefix = path_tag

            if new_challenge.upload:
                if new_challenge.hosted: 
                    
                    image_name = path_tag + ':latest'
                    new_challenge.imageName = image_name
                    
                    #build image
                    build = d.buildImage(fileobj=form.cleaned_data['upload'].file, tag=path_tag)

                    #if build fails set vars as such
                    if not build:
                        error_msg = "****build image failed****"
                        new_challenge.pathPrefix = error_msg
                        new_challenge.imageName = error_msg

                    new_challenge.upload.save(form.cleaned_data['upload'].name,form.cleaned_data['upload'])
                    rethink_data = {'sid': new_challenge.id, 'category': new_challenge.category.id, 'title': new_challenge.title, 'points': new_challenge.points, 'description': new_challenge.description, 'hosted': new_challenge.hosted,
                                    'fileUpload': new_challenge.fileUpload, 'imageName': new_challenge.imageName, 'ports': new_challenge.ports, 'pathPrefix': new_challenge.pathPrefix, 'created': format(new_challenge.created, 'U')}
                
                elif new_challenge.fileUpload:
                    print('fileUpload')
                    new_challenge.upload.save(
                        form.cleaned_data['upload'].name, form.cleaned_data['upload'])
                    rethink_data = {'sid': new_challenge.id, 'category': new_challenge.category.id, 'title': new_challenge.title, 'points': new_challenge.points, 'description': new_challenge.description, 'hosted': new_challenge.hosted,
                                    'fileUpload': new_challenge.fileUpload, 'pathPrefix': new_challenge.pathPrefix, 'downloadPath': new_challenge.upload.url, 'created': format(new_challenge.created, 'U')}
            else:
                #doesn't have a file uploaded
                rethink_data = {'sid': new_challenge.id, 'category': new_challenge.category.id, 'title': new_challenge.title, 'points': new_challenge.points, 'description': new_challenge.description, 'hosted': new_challenge.hosted,
                                    'fileUpload': new_challenge.fileUpload, 'imageName': new_challenge.imageName, 'ports': new_challenge.ports, 'pathPrefix': new_challenge.pathPrefix, 'created': format(new_challenge.created, 'U')}
                                    
            new_challenge.save()

            # Push the realtime data to rethinkdb
            connection = r.connect(host=RDB_HOST, port=RDB_PORT)
            try:
                r.db(CTF_DB).table('challenges').insert(
                    rethink_data).run(connection)
            except RqlRuntimeError as e:
                #raise Exception('Error adding challenge to realtime database: %s' % (e))
                print('Error adding challenge to realtime database: %s' % (e))
            finally:
                connection.close()


            return redirect('challenge_detail', pk=new_challenge.pk)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ChallengeForm()

    return render(request, 'adminpanel/challenges/challenge_edit.html', {'form': form})

@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def challenge_edit(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk)
    if request.method == "POST":
        form = ChallengeForm(request.POST, request.FILES, instance=challenge)

        # check whether it's valid:
        if form.is_valid():

            if form.has_changed():

                # prepare challenge object for saving
                new_challenge = form.save(commit=False)

                rethink_updates = {}

                hosted_update_needed = False
                fileUpload_update_needed = False
                upload_update_needed = False
                for i in form.changed_data:
                    if i == 'hosted':
                        print ('hosted change')
                        hosted_update_needed = True                    
                        
                    elif i == 'fileUpload':
                        print ('fileUpload change')
                        fileUpload_update_needed = True
                        
                    elif i == 'upload':
                        print ('uploaded file changed')
                        upload_update_needed = True
                        
                    elif i == 'points':
                        print('points changed')
                        rethink_updates[i] = form.cleaned_data[i]
                        u = updatePoints(new_challenge, form.initial['points'])
                        print('update points: {0}'.format(u))
                        
                    else:
                        #but don't update the fields that get auto updated ^
                        if i != 'upload':
                            rethink_updates[i] = form.cleaned_data[i]

                if hosted_update_needed:
                    rethink_updates['hosted'] = new_challenge.hosted
                    if not new_challenge.hosted :
                        # new_challenge.pathPrefix = ''
                        # rethink_updates['pathPrefix'] = ''

                        new_challenge.imageName = ''
                        rethink_updates['imageName'] = ''

                        new_challenge.ports = ''
                        rethink_updates['ports'] = ''

                        if not new_challenge.fileUpload:  
                            new_challenge.upload = None
                                            
                    
                if fileUpload_update_needed:
                    rethink_updates['fileUpload'] = new_challenge.fileUpload
                    
                    if not new_challenge.fileUpload: 
                        # new_challenge.upload = None
                        rethink_updates['downloadPath'] = ''
                        
                        if not new_challenge.hosted:
                            new_challenge.upload = None

                if upload_update_needed:
                    print ('executing update')
                    
                    if form.cleaned_data['upload']:
                        #set var for pathPrefix and tag
                        #path_tag = str(new_challenge.id) + '_' + re.sub('[^A-Za-z0-9]+', '', new_challenge.category.name.lower()) + str(new_challenge.points)
                        path_tag = 'chall_' + str(new_challenge.id)
                        new_challenge.pathPrefix = path_tag
                        rethink_updates['pathPrefix'] = path_tag

                        if new_challenge.hosted: 
                            image_name = path_tag + ':latest'
                            new_challenge.imageName = image_name
                            rethink_updates['imageName'] = image_name
                    
                            #build image
                            build = d.buildImage(fileobj=form.cleaned_data['upload'].file, tag=path_tag)

                            #if build fails set vars as such
                            if not build:
                                error_msg = "****build image failed****"
                                new_challenge.pathPrefix = error_msg
                                rethink_updates['pathPrefix'] = error_msg
                                new_challenge.imageName = error_msg
                                rethink_updates['imageName'] = error_msg
                        
                        # save the uploaded file
                        new_challenge.upload.save(form.cleaned_data['upload'].name,form.cleaned_data['upload'])
                            
                        if new_challenge.hosted:
                            try:
                                ports = list()
                                for line in new_challenge.upload.file:
                                    line = line.decode('utf-8')
                                    start = 'EXPOSE '

                                    if (start in line):
                                        possible_port = (line[line.find(start)+len(start):])
                                        ports.append(possible_port.split())

                                # flatten list
                                flattened_ports = list(set([val for sublist in ports for val in sublist]))
                                print (flattened_ports)

                                if len(flattened_ports):
                                    new_challenge.ports = flattened_ports
                                    rethink_updates['ports'] = flattened_ports
                                else:
                                    new_challenge.ports = '****no exposed ports****'
                                    rethink_updates['ports'] = '****no exposed ports****'

                            except Exception as e:
                                #raise Exception('Error parsing uploaded Dockerfile: ', e)
                                print ('Error parsing uploaded Dockerfile: ', e)
                                new_challenge.ports = '****error parsing ports****'
                                rethink_updates['ports'] = '****error parsing ports****'
                                
                        
                    
                        if new_challenge.fileUpload: 
                            
                            rethink_updates['downloadPath'] = new_challenge.upload.url
                            
                    # else:
                    #     #file removed from object
                    #     #accept user values for ports and imageName
                    #     #set pathPrefix to null
                    #     new_challenge.pathPrefix = ''
                    #     rethink_updates['pathPrefix'] = ''


                print(rethink_updates)

                connection = r.connect(host=RDB_HOST, port=RDB_PORT)
                if len(rethink_updates) != 0:
                    try:
                        r.db(CTF_DB).table('challenges').filter( {'sid': new_challenge.id} ).update(rethink_updates).run(connection)
                    except RqlRuntimeError as e:
                        #raise Exception('Error updating challenge from realtime database: %s' % (e))
                        print('Error updating challenge from realtime database: %s' % (e))
                    finally:
                        connection.close()

                new_challenge.save()


            # redirect to challenge detail page
            return redirect('challenge_detail', pk=form.instance.pk)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ChallengeForm(instance=challenge)

    return render(request, 'adminpanel/challenges/challenge_edit.html', {'form': form})
############################################

################## ctfs ###################
@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def ctf_list(request):
    ctfs = Ctf.objects.all().order_by('created')
    return render(request, 'adminpanel/ctfs/ctf_list.html', {'ctfs' : ctfs})

@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def ctf_detail(request, pk):
    ctf = get_object_or_404(Ctf, pk=pk)
    return render(request, 'adminpanel/ctfs/ctf_detail.html', {'ctf': ctf})

@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def ctf_delete(request, pk):
    ctf = get_object_or_404(Ctf, pk=pk)

    #try rethink delete, then django delete
    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    try:
        r.db(CTF_DB).table('ctfs').filter({'sid':ctf.id}).delete().run(connection)
        ctf.delete()
    except Exception as e:
        #raise Exception('Error deleting ctf from realtime database: %s' % (e))
        print('Error deleting ctf: %s' % (e))
    finally:
        connection.close()

    return redirect(ctf_list)

@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def ctf_new (request):

    if request.method == 'POST':
        form = CtfForm(request.POST)
        if form.is_valid():

            #create ctf object
            new_ctf = form.save()

            # Push ctf to rethinkdb database
            connection = r.connect(host=RDB_HOST, port=RDB_PORT)
            try:
                r.db(CTF_DB).table('ctfs').insert({ 'sid': new_ctf.id, 'start': format(new_ctf.start, 'U'), 'end': format(new_ctf.end, 'U'), 'created': format(new_ctf.created, 'U')}).run(connection)
            except Exception as e:
                raise Exception('Error adding ctf: %s' % (e))
            finally:
                connection.close()


            return redirect('ctf_detail', pk=new_ctf.pk)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CtfForm()

    return render(request, 'adminpanel/ctfs/ctf_edit.html', {'form': form})

@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def ctf_edit(request, pk):
    ctf = get_object_or_404(Ctf, pk=pk)
    if request.method == "POST":
        form = CtfForm(request.POST, instance=ctf)
        # check whether it's valid:
        if form.is_valid():

            if form.has_changed():

                # save ctf object
                new_ctf = form.save()

                rethink_updates = {}

                for i in form.changed_data:
                    #only edit datetimes in ctf model so format everything as such (will need to update as add more to model)
                    rethink_updates[i] = format(form.cleaned_data[i], 'U')

                print(rethink_updates)

                connection = r.connect(host=RDB_HOST, port=RDB_PORT)
                if len(rethink_updates) != 0:
                    try:
                        r.db(CTF_DB).table('ctfs').filter( {'sid': new_ctf.id} ).update(rethink_updates).run(connection)
                    except RqlRuntimeError as e:
                        #raise Exception('Error updating ctf from realtime database: %s' % (e))
                        print('Error updating ctf from realtime database: %s' % (e))
                    finally:
                        connection.close()
        
            # redirect to ctf detail page
            return redirect('ctf_detail', pk=new_ctf.pk)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = CtfForm(instance=ctf)

    return render(request, 'adminpanel/ctfs/ctf_edit.html', {'form': form})

############################################

################ containers ################
@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def container_list(request):
    containers = Container.objects.all().order_by('created')
    return render(request, 'adminpanel/containers/container_list.html', {'containers' : containers})

# @xframe_options_exempt
# @user_passes_test(lambda u: u.is_superuser)
# def container_detail(request, pk):
#     container = get_object_or_404(Container, pk=pk)
#     return render(request, 'containers/container_detail.html', {'container': container})

# @xframe_options_exempt
# @user_passes_test(lambda u: u.is_superuser)
# def container_delete(request, pk):
#     container = get_object_or_404(Container, pk=pk)
#     container.delete()
#     return redirect(container_list)

# @xframe_options_exempt
# @user_passes_test(lambda u: u.is_superuser)
# def container_new (request):

#     if request.method == 'POST':
#         form = ContainerForm(request.POST)
#         if form.is_valid():
#             new_container = form.save()

#             return redirect('container_detail', pk=new_container.pk)

#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = ContainerForm()

#     return render(request, 'containers/container_edit.html', {'form': form})

# @xframe_options_exempt
# @user_passes_test(lambda u: u.is_superuser)
# def container_edit(request, pk):
    # container = get_object_or_404(Container, pk=pk)
    # if request.method == "POST":
    #     form = ContainerForm(request.POST, instance=container)
    #     # check whether it's valid:
    #     if form.is_valid():
    #         # save the for to the db
    #         new_container = form.save()

    #         # redirect to container detail page
    #         return redirect('container_detail', pk=new_container.pk)

    # # if a GET (or any other method) we'll create a blank form
    # else:
    #     form = ContainerForm(instance=container)

    # return render(request, 'adminpanel/containers/container_edit.html', {'form': form})
############################################

################## teams ###################
@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def team_list(request):
    teams = Team.objects.select_related().all().order_by('created')

    return render(request, 'adminpanel/teams/team_list.html', {'teams' : teams})

@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    return render(request, 'adminpanel/teams/team_detail.html', {'team': team})

@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def team_delete(request, pk):
    team = get_object_or_404(Team, pk=pk)

    #try rethink delete, then django delete
    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    try:
        r.db(CTF_DB).table('teams').filter({'sid':team.id}).delete().run(connection)
        team.delete()
    except Exception as e:
        #raise Exception('Error deleting team from realtime database: %s' % (e))
        print('Error deleting team: %s' % (e))
    finally:
        connection.close()

    return redirect(team_list)

@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def team_new (request):

    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():

            #create team object but don't commit
            new_team = form.save(commit=False)

            # Create unique team token
            token = str(uuid.uuid4())
            while Team.objects.filter(token__iexact=token).exists():
                token = str(uuid.uuid4())

            new_team.token = token
            #commit so that you have team.id
            new_team.save()
            #have to specifically save many-to-many relationships when using commit=False
            form.save_m2m()

            # Push team to rethinkdb database
            connection = r.connect(host=RDB_HOST, port=RDB_PORT)
            try:
                r.db(CTF_DB).table('teams').insert({ 'sid': new_team.id, 'name': new_team.name, 'token': token, 'points': new_team.points, 'hidden': new_team.hidden, 'correct_flags': new_team.correct_flags, 'wrong_flags': new_team.wrong_flags, 'solved': [], 'created': format(new_team.created, 'U')}).run(connection)
            except Exception as e:
                raise Exception('Error adding team: %s' % (e))
            finally:
                connection.close()


            return redirect('team_detail', pk=new_team.pk)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TeamForm()

    return render(request, 'adminpanel/teams/team_edit.html', {'form': form})

@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def team_edit(request, pk):
    team = get_object_or_404(Team, pk=pk)
    if request.method == "POST":
        form = TeamForm(request.POST, instance=team)
        # check whether it's valid:
        if form.is_valid():

            if form.has_changed():

                # save team object
                new_team = form.save()

                rethink_updates = {}

                for i in form.changed_data:
                    rethink_updates[i] = form.cleaned_data[i]

                print(rethink_updates)

                connection = r.connect(host=RDB_HOST, port=RDB_PORT)
                if len(rethink_updates) != 0:
                    try:
                        r.db(CTF_DB).table('teams').filter( {'sid': new_team.id} ).update(rethink_updates).run(connection)
                    except RqlRuntimeError as e:
                        #raise Exception('Error updating team from realtime database: %s' % (e))
                        print('Error updating team from realtime database: %s' % (e))
                    finally:
                        connection.close()
        
            # redirect to team detail page
            return redirect('team_detail', pk=new_team.pk)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = TeamForm(instance=team)

    return render(request, 'adminpanel/teams/team_edit.html', {'form': form})

############################################

################## users ###################
@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def user_list(request):
    users = User.objects.all().order_by('created')
    return render(request, 'adminpanel/users/user_list.html', {'users' : users})

@xframe_options_exempt
@user_passes_test(lambda u: u.is_superuser)
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    return render(request, 'adminpanel/users/user_detail.html', {'user': user})

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

    return render(request, 'adminpanel/users/user_edit.html', {'form': form})

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

    return render(request, 'adminpanel/users/user_edit.html', {'form': form})

############################################





def getDjangoTeamsWithSolvedChallengesByID(chal_id):

    # get the django team object
    if Team.objects.filter(solved__challenge_id=chal_id).exists():
        teams = Team.objects.filter(solved__challenge_id=chal_id)
        return teams
    else:
        return False


def updatePoints(new_challenge, initial_points):

    teams = getDjangoTeamsWithSolvedChallengesByID(new_challenge.id) 
    
    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    rethink_updates = {}
   
    if teams:
        try:
            for team in teams: 
                print('Updating {0}\'s points.'.format(team.name))  
                        
                # calculate the difference in points from old points value to new.
                chal_diff_points = abs(new_challenge.points - initial_points)
                rethink_teams = r.db(CTF_DB).table('teams').filter({'sid':team.id}).run(connection)    

                # use for loop to access the object(s) values and assign to team id variable
                for rethink_team in rethink_teams: 
                    # print(rethink_team['id'])   
                    rethink_team_id = rethink_team['id']
                
                rethink_team_object = r.db('redctf').table(
                'teams').get(rethink_team_id).run(connection)
                
                # get rethink team solved object 
                solved_object = rethink_team_object['solved']
                
                # print(rethink_team_id)
            
                
                # if the initial points value is less than the new value for the challenge add the chal_diff_points to team's total points
                if initial_points < new_challenge.points:
                    # update total team points
                    team.points += chal_diff_points
                    
                # if the initial points value is greater than the new value for the challenge subtract the chal_diff_points to team's total points
                elif initial_points > new_challenge.points:
                    # update total team points
                    team.points -= chal_diff_points

                else:
                    print('no points change')
                    #raise Exception('updated points value is equal to the existing points value')
                    print('updated points value is equal to the existing points value')
                
                # set backend updated team points
                team.save()
                
                # set update for rethinkdb team points
                rethink_updates['points'] = team.points
                
                # update the team's solved challenge points
                solved_challenge = team.solved.get(challenge_id=new_challenge.id)
                solved_challenge.points = new_challenge.points
                
                
                # find challenges to update within rethink solved object
                for index, rethink_solved_chall in enumerate(solved_object):
                    if rethink_solved_chall['id'] == new_challenge.id:
                        solved_object[index]['points'] = new_challenge.points
                
                # update solved object for rethink update
                rethink_updates['solved'] = solved_object
                
                # run updates on rethink
                update = r.db('redctf').table('teams') \
                    .get(rethink_team_id)\
                    .update(rethink_updates).run(connection)
                print('updates: {0}'.format(update))

        except Exception as ex:
            #raise Exception('error with teams')
            print('error with teams')
            
    else:
        print('no matching teams ')
   
    return True
