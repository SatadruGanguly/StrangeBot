from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.contrib.auth.hashers import check_password

import os
import cv2
from PIL import Image as im
import numpy as np
from datetime import date, datetime, time
import re
import mimetypes

from .models import MyUser, ChatRecords, GuestChatRecords
from .forms import *
from .mydecorators import auth_required, unauth_required
from MedBotProject.settings import STATIC_DIR, MEDIA_DIR, BASE_DIR

from DL.red_eye_recognition_and_Expression import Eye_Evaluation, detect_Expression
from NLP import ChatBot

# Create your views here.
def index(request):
    TEMP_DIR = os.path.join(STATIC_DIR, 'MedBotApp', 'temp_images')
    for f in os.listdir(TEMP_DIR):
        os.remove(os.path.join(TEMP_DIR, f))
    # ChatBot.test()
    # my_dict=['j', 'yo']
    
    return render(request, 'MedBotApp/index.html')


@unauth_required
def user_register(request):
    user_reg_form = RegistrationForm()
    myuser_reg_form = MyUserForm()
    context_dict = {
        'user_reg_form': user_reg_form,
        'myuser_reg_form': myuser_reg_form,
    }
    if request.method == 'POST':
        user_reg_form = RegistrationForm(request.POST)
        myuser_reg_form = MyUserForm(request.POST)
        if user_reg_form.is_valid() and myuser_reg_form.is_valid():
            if user_reg_form.cleaned_data['password'] == user_reg_form.cleaned_data['reenter_pass']:
                user = user_reg_form.save()
                user.set_password(user.password)
                user.save()
                myuser = myuser_reg_form.save(commit=False)
                myuser.user_ref = user
                myuser.save()
                return redirect('index')
            else:
                context_dict = {
                    'error_status': 1,
                    'error_msg': 'Error occured during registration',
                    'extra_msg': 'Passwords do not match',
                    'back_url': '/register',
                }
                return render(request, 'MedBotApp/error.html', context=context_dict)
        else:
            context_dict = {
                    'error_status': 1,
                    'error_msg': 'Error occured during registration',
                    'extra_msg': str(user_reg_form.errors)+'\n'+str(myuser_reg_form.errors),
                    'back_url': '/register',
                }
            return render(request, 'MedBotApp/error.html', context=context_dict)
    return render(request, 'MedBotApp/register.html', context=context_dict)


@unauth_required
def user_login(request):
    login_form = LoginForm()
    if request.method == 'POST':
        filled_form = LoginForm(request.POST)
        if filled_form.is_valid():
            username = filled_form.cleaned_data['username']
            password = filled_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    # print('Here1')
                    return redirect('index')
                else:
                    # print('Here2')
                    context_dict = {
                        'error_status': 1,
                        'error_msg': 'Error occured during login',
                        'extra_msg': 'Account Not Active',
                        'back_url': '/login',
                    }
                    return render(request, 'MedBotApp/error.html', context=context_dict)
            else:
                # print('Here3')
                context_dict = {
                        'error_status': 1,
                        'error_msg': 'Error occured during login',
                        'extra_msg': 'Invalid Username or Password',
                        'back_url': '/login',
                }
                return render(request, 'MedBotApp/error.html', context=context_dict)
    else:
        return render(request, 'MedBotApp/login.html', {'login_form': login_form})

@auth_required
def user_logout(request):
    logout(request)
    return redirect('index')    


@auth_required
def accountInfo(request):
    user = User.objects.filter(username=request.user.username)[0]
    myuser = MyUser.objects.filter(user_ref=user)[0]
    # print(context_dict['gender'])
    if request.method == 'POST':
        fn = request.POST['fn']
        ln = request.POST['ln']
        g = request.POST['g']
        dob = request.POST['dob']
        print(fn,' ', ln, ' ', g, ' ', dob)
        user.first_name = fn
        user.last_name = ln
        myuser.gender = g
        myuser.dob = dob
        user.save()
        myuser.save()
        user = User.objects.filter(username=request.user.username)[0]
        myuser = MyUser.objects.filter(user_ref=user)[0]
    
    context_dict = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'gender': myuser.gender,
        'dob': str(myuser.dob),
    }
    return render(request, 'MedBotApp/account.html', context=context_dict)


@auth_required
def changePassword(request):
    user = User.objects.filter(username=request.user.username)[0]
    if request.method == 'POST':
        cp = request.POST['cp']
        if check_password(cp, user.password):
            np = request.POST['np']
            rnp = request.POST['rnp']
            if np == rnp:
                user.set_password(np)
                user.save()
                user = User.objects.filter(username=request.user.username)[0]
                context_dict = {
                    'success_status': 1,
                    'success_msg': 'Password changed successfully',
                    'extra_msg': 'You\'ll be logged out in 5 secounds...',
                }
                return render(request, 'MedBotApp/success.html', context=context_dict)
            else:
                context_dict = {
                    'error_status': 1,
                    'error_msg': 'New Passwords don\'t match.',
                    'back_url': '/changePassword',
                }
                return render(request, 'MedBotApp/error.html', context=context_dict)
        else:
            context_dict = {
                    'error_status': 1,
                    'error_msg': 'Incorrect current password.',
                    'extra_msg': 'Contact Website administrator if you\'ve forgotten your password',
                    'back_url': '/changePassword',
                }
            return render(request, 'MedBotApp/error.html', context=context_dict)
    return render(request, 'MedBotApp/change_password.html')


@auth_required
def downloadTranscript(request):
    user = User.objects.filter(username=request.user.username)[0]
    myuser = MyUser.objects.filter(user_ref=user)[0]
    chats = ChatRecords.objects.filter(user_ref=myuser).order_by('sentat')
    dtime = datetime.now()
    file_name = user.username + '_transcript_' + dtime.strftime('%Y%m%d%H%M%S') + '.txt'
    file_relative_path = os.path.join('MedBotApp', 'chat_downloads', file_name)
    file_absolute_path = os.path.join(STATIC_DIR, file_relative_path)
    f = open(file_absolute_path, 'w')
    f.write('Chat transcript of {}, created and download at {}\n'.format(user.username, dtime.strftime('%H:%M:%S, %d-%m-%Y')))
    f.write(' \n')
    for chat in chats:
        if chat.sentby == 'Dummy':
            f.write('\n')
        else:
            msg = '({}) {}: {}\n'.format(chat.sentat, chat.sentby, chat.message)
            f.write(msg)
    f.write('\nFile Generated by PokehBot - The NextGen MedBot')
    f.close()
    f = open(file_absolute_path, 'r')
    mime_type, _ = mimetypes.guess_type(file_absolute_path)
    response = HttpResponse(f, content_type=mime_type)
    response['Content-Disposition'] = "attachment; filename=%s" % file_name
    return response


def chatModelDecider(request):
    if request.user.is_authenticated:
        return chatWindow(request)
    else:
        return guestChatWindow(request)


def chatWindow(request):
    user = User.objects.filter(username=request.user.username)[0]
    myuser = MyUser.objects.filter(user_ref=user)[0]
    chats = ChatRecords.objects.filter(user_ref=myuser).order_by('sentat')
    if len(chats) == 0:
        start = ChatRecords(user_ref=myuser, message='---', sentby='Dummy')
        start.save()
        chats = ChatRecords.objects.filter(user_ref=myuser).order_by('sentat')
    
    if request.method == 'POST':
        filled_form = ChatForm(request.POST)
        if filled_form.is_valid():
            # print('User Message : '+filled_form.cleaned_data['message'])
            form_data = filled_form.save(commit=False)
            form_data.user_ref = myuser
            form_data.sentby = 'User'
            form_data.save()
            reply_msg, symp_list = ChatBot.getSymptoms(form_data.message)
            reply = ChatRecords(user_ref=myuser, message=reply_msg, sentby='Bot')
            reply.save()
            if symp_list:
                d, p, t = ChatBot.getResponse(symp_list)
                reply = ChatRecords(user_ref=myuser, message=d, sentby='Bot')
                reply.save()
                reply = ChatRecords(user_ref=myuser, message=p, sentby='Bot')
                reply.save()
                reply = ChatRecords(user_ref=myuser, message=t, sentby='Bot')
                reply.save()

            end = ChatRecords(user_ref=myuser, message='---', sentby='Dummy')
            end.save()
    
    if chats and ChatRecords.objects.last().sentby == 'Dummy':
        welcome = ChatRecords(user_ref=myuser, message=ChatBot.welcome(), sentby='Bot')
        welcome.save()
    
    chats = ChatRecords.objects.filter(user_ref=myuser).order_by('sentat')
    form = ChatForm()
    context_dict = {'chats': chats, 'form': form}
    
    return render(request, 'MedBotApp/chat.html', context=context_dict)


def guestChatWindow(request):
    guest_id = 'guest_'+str(datetime.now())
    if 'guest_id' in request.session.keys():
        guest_id = request.session['guest_id']
    else:
        request.session['guest_id'] = guest_id
    
    delete_recs = GuestChatRecords.objects.exclude(guest_ref=guest_id)
    if delete_recs:
        delete_recs.delete()
    guest_chats = GuestChatRecords.objects.filter(guest_ref=guest_id).order_by('sentat')
    if len(guest_chats) == 0:
        start = GuestChatRecords(guest_ref=guest_id, message='---', sentby='Dummy')
        start.save()
        guest_chats = GuestChatRecords.objects.filter(guest_ref=guest_id).order_by('sentat')
    
    if request.method == 'POST':
        filled_form = GuestChatForm(request.POST)
        if filled_form.is_valid():
            # print('User Message : '+filled_form.cleaned_data['message'])
            chat = GuestChatRecords(guest_ref=guest_id, message=filled_form.cleaned_data['message'], sentby='User')
            chat.save()
            
            reply_msg, symp_list = ChatBot.getSymptoms(filled_form.cleaned_data['message'])
            reply = GuestChatRecords(guest_ref=guest_id, message=reply_msg, sentby='Bot')
            reply.save()
            
            if symp_list:
                d, p, t = ChatBot.getResponse(symp_list)
                reply = GuestChatRecords(guest_ref=guest_id, message=d, sentby='Bot')
                reply.save()
                reply = GuestChatRecords(guest_ref=guest_id, message=p, sentby='Bot')
                reply.save()
                reply = GuestChatRecords(guest_ref=guest_id, message=t, sentby='Bot')
                reply.save()
                        
            start = GuestChatRecords(guest_ref=guest_id, message='---', sentby='Dummy')
            start.save()
    # print(guest_chats)
    if guest_chats and GuestChatRecords.objects.last().sentby == 'Dummy':
        welcome = GuestChatRecords(guest_ref=guest_id, message=ChatBot.welcome(), sentby='Bot')
        welcome.save()
    
    guest_chats = GuestChatRecords.objects.filter(guest_ref=guest_id).order_by('sentat')
    form = ChatForm()
    context_dict = {'chats': guest_chats, 'form': form}
    
    return render(request, 'MedBotApp/chat.html', context=context_dict)



@auth_required
def imageAnalysis(request):
    return render(request, 'MedBotApp/image_analysis.html')


@auth_required
def eyeAnalysis(request):
    user = User.objects.filter(username=request.user.username)[0]
    myuser = MyUser.objects.filter(user_ref=user)[0]
    
    form = ImageForm()
    test_img_url = os.path.join('MedBotApp', 'test_images', 'irritated-red-eyes-needs-sterile-eye-drops_8595-3005.jpg')
    # print(test_img_url)

    context_dict = {'form': form, 'flag': 0, 'test_img_url': test_img_url}
    if request.method == 'POST':
        filled_form = ImageForm(request.POST, request.FILES)
        if filled_form.is_valid():
            # Generate FileName using TimeStamp
            timestamp = re.sub(r'[-:.\s]', '', str(datetime.now()))
            user_image_file_name = myuser.user_ref.username + '_eye_' + timestamp + '.jpg'
            bot_image_file_name = 'b_' + user_image_file_name
            temp_botFile_relative_URL = os.path.join('MedBotApp', 'temp_images', bot_image_file_name)
            temp_botFile_absolute_URL = os.path.join(STATIC_DIR, temp_botFile_relative_URL)

            # Extract and Evaluate User Image
            user_img = filled_form.cleaned_data['user_image']
            result_image, result_status, result_msg = Eye_Evaluation(cv2.imdecode(np.fromstring(user_img.read(), np.uint8), cv2.IMREAD_UNCHANGED))      
            
            if result_status == 1:   
                # Write it temporarily to the static directory
                cv2.imwrite(temp_botFile_absolute_URL, result_image)

                # Get form data
                form_data = filled_form.save(commit=False)

                # Fill / Re-fill Form Data
                form_data.user_ref = myuser
                form_data.user_image = user_img
                form_data.user_image.name = user_image_file_name

                # Create Temporary file, write the result image to it and save to form field
                img_temp = NamedTemporaryFile()
                img_temp.write(open(temp_botFile_absolute_URL, 'rb').read())
                img_temp.flush()
                form_data.bot_image.save(bot_image_file_name, img_temp)
                
                form_data.purpose = 'Eye'
                form_data.result = result_msg
                
                # Submit Form Data
                form_data.save()

                # print('BOT FILE : ', temp_botFile_absolute_URL)

                # cv2.imshow('window', result_image)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
                context_dict['result_image'] = temp_botFile_relative_URL

            context_dict['result_msg'] = result_msg
            context_dict['result_status'] = result_status
            context_dict['flag'] = 1

            return render(request, 'MedBotApp/eye_analysis.html', context=context_dict)
        else:
            return HttpResponse('Form invalid : ', filled_form.errors)

    return render(request, 'MedBotApp/eye_analysis.html', context=context_dict)


@auth_required
def moodDetection(request):
    user = User.objects.filter(username=request.user.username)[0]
    myuser = MyUser.objects.filter(user_ref=user)[0]
    form = ImageForm()
    context_dict = {'form': form, 'flag': 0}
    if request.method == 'POST':
        filled_form = ImageForm(request.POST, request.FILES)
        if filled_form.is_valid():
            # Generate FileName using TimeStamp
            timestamp = re.sub(r'[-:.\s]', '', str(datetime.now()))
            user_image_file_name = myuser.user_ref.username + '_exp_' + timestamp + '.jpg'
            
            # Extract and Evaluate User Image
            user_img = filled_form.cleaned_data['user_image']
            user_img_decoded = cv2.imdecode(np.fromstring(user_img.read(), np.uint8), cv2.IMREAD_UNCHANGED)
            expression_msg = detect_Expression(user_img_decoded)

            # Get form data
            form_data = filled_form.save(commit=False)

            # Fill / Re-fill Form Data
            form_data.user_ref = myuser
            form_data.user_image = user_img
            form_data.user_image.name = user_image_file_name

            form_data.purpose = 'Exp'
            form_data.result = expression_msg
            
            # Submit Form Data
            form_data.save()

            # Write it temporarily to the static directory
            temp_botFile_relative_URL = os.path.join('MedBotApp', 'temp_images', user_image_file_name)
            temp_botFile_absolute_URL = os.path.join(STATIC_DIR, temp_botFile_relative_URL)
            cv2.imwrite(temp_botFile_absolute_URL, user_img_decoded)
            context_dict['user_img_url'] = temp_botFile_relative_URL
            context_dict['exp_msg'] = expression_msg
            context_dict['flag'] = 1

            # return render(request, 'MedBotApp/mood_detection.html', context=context_dict)
        else:
            return HttpResponse('Form invalid : ', filled_form.errors)

    return render(request, 'MedBotApp/mood_detection.html', context=context_dict)
