"""MedBotProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from MedBotApp import views
from MedBotProject import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', views.index, name='index'),
    
    path('register', views.user_register, name='user_regiser'),
    path('login', views.user_login, name='user_login'),
    path('logout', views.user_logout, name='user_logout'),
    
    path('account', views.accountInfo, name='account_info'),
    path('changePassword', views.changePassword, name='change_password'),
    path('downloadTranscript', views.downloadTranscript, name='download_transcript'),
    
    path('chat', views.chatModelDecider, name='chatWindow'),
    
    path('image_analysis', views.imageAnalysis, name='imageAnalysis'),
    path('eye_analysis', views.eyeAnalysis, name='eyeAnalysis'),
    path('mood_detection', views.moodDetection, name='moodDetection'),
]
