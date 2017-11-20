from django import forms
from . import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class RegistrationForm(forms.ModelForm):

    username = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Username', 'class':"form-control"}))
    first_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'First Name', 'class':"form-control"}))
    last_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Last Name', 'class':"form-control"}))
    email = forms.EmailField(required=True, widget=forms.widgets.TextInput(attrs={'placeholder': 'Email', 'class':"form-control"}))
    password1 = forms.CharField(required=True, widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Password', 'class':"form-control"}))
    password2 = forms.CharField(required=True, widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class':"form-control"}))

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )
    def clean_email(self):
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(("This email address is already in use. Please supply a different email address."))
        return self.cleaned_data['email']


class CreatePostForm(forms.ModelForm):
    content = forms.CharField(max_length=42, widget=forms.widgets.TextInput(attrs={'placeholder': 'Say something here', 'class':"form-control"}))

    class Meta: 
        model= models.Post
        exclude = ('user_name',)

class CreatePostForm(forms.ModelForm):
    content = forms.CharField(max_length=42, widget=forms.widgets.TextInput(attrs={'placeholder': 'Comment this post', 'class':"form-control"}))
    
    class Meta: 
        model= models.Comment
        exclude = ('user_name',)

class UpdateProfil(forms.ModelForm):
    first_name = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'First Name', 'class':"form-control"}))
    last_name = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Last Name', 'class':"form-control"}))
    age = forms.IntegerField(widget=forms.widgets.TextInput(attrs={'placeholder': 'Age', 'class':"form-control"}))
    bio = forms.CharField(required=False,widget=forms.widgets.TextInput(attrs={'placeholder': 'Describe yourself (420 character max.)', 'class':"form-control"}))
    password = forms.CharField(required=False, widget=forms.widgets.PasswordInput(attrs={'placeholder': 'New Password', 'class':"form-control"}))
    picture = forms.ImageField()


    class Meta:
        model = models.UserProfil
        exclude = ('user','followees', )