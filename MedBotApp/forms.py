from django import forms
from django.contrib.auth.models import User
from django.forms import widgets
from django.contrib.auth.models import User

from .models import ChatRecords, GuestChatRecords, ImageRecords, MyUser

# Create your forms here.
class RegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.Meta.required:
            self.fields[field].required = True
    
    reenter_pass = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Re-Enter Password'}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter your First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter your Last Name'}),
            'username': forms.TextInput(attrs={'placeholder': 'Enter unique Username'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter Password'}),
        }
        required = {
            'first_name', 
            'last_name', 
            'username', 
            'password',
            'reenter_pass',
        }


class MyUserForm(forms.ModelForm):
    check1 = forms.BooleanField(required = True, 
                                label='I consent StrangeBot to collect and store personal and medical data provided by me.')
    check2 = forms.BooleanField(required = True, 
                                label='I understand that the information provided by StrangeBot should not be considered as professional medical advice. I should always visit a registered medical practitioner if needed.')
    class Meta:
        model = MyUser
        fields = ['gender', 'dob']
        widgets = {
            'gender': forms.RadioSelect(),
            'dob': forms.DateInput(attrs={'type': 'date'}),
        }


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs=({'placeholder': 'Username'})))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class ChatForm(forms.ModelForm):
    class Meta:
        model = ChatRecords
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'placeholder': 'What\'s bothering you?',
                                            'rows': 1})
        }
    # message = forms.CharField(max_length=1000, widget=forms.TextInput(attrs={'placeholder': 'What\'s bothering you?'}))


class GuestChatForm(forms.ModelForm):
    class Meta:
        model = GuestChatRecords
        fields = ['message']
        widgets = {
            'message': forms.TextInput(attrs={'placeholder': 'What\'s bothering you?'})
        }
        

class ImageForm(forms.ModelForm):
    class Meta:
        model = ImageRecords
        fields = ['user_image']