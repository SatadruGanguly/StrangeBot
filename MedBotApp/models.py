from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class MyUser(models.Model):
    user_ref = models.OneToOneField(User, on_delete=models.CASCADE)
    GENDERS = (('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others'))
    gender = models.CharField(default=GENDERS[0][0], choices=GENDERS, max_length=10)
    dob = models.DateField(default=datetime.date.today())

    def __str__(self):
        return self.user_ref.username


class ChatRecords(models.Model):
    user_ref = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)
    
    SENT_BY = (('Bot', 'Bot'), ('User', 'User'), ('Dummy', 'Dummy'))
    sentby = models.CharField(blank=True, choices=SENT_BY, max_length=10)
    
    sentat = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "{}, {}, {}".format(self.user_ref.user_ref.username, self.sentby, str(self.sentat))


class GuestChatRecords(models.Model):
    guest_ref = models.CharField(max_length=20)
    message = models.CharField(max_length=1000)
    
    SENT_BY = (('Bot', 'Bot'), ('User', 'User'), ('Dummy', 'Dummy'))
    sentby = models.CharField(blank=True, choices=SENT_BY, max_length=10)
    
    sentat = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "{}, {}, {}".format(self.guest_ref, self.sentby, str(self.sentat))


class ImageRecords(models.Model):
    user_ref = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    user_image = models.ImageField(upload_to='user_images')
    bot_image = models.ImageField(blank=True, upload_to='bot_images')

    PURPOSES = (('Eye', 'Eye'), ('Exp', 'Exp'))
    purpose = models.CharField(blank=True, choices=PURPOSES, max_length=3)
    result = models.CharField(max_length=150)

    checked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}, {}, {}".format(self.user_ref.user_ref.username, self.purpose, self.checked_at)
