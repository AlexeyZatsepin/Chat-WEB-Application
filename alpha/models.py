from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms


class Profile(User):
    image = models.ImageField(upload_to='images')


class Chat(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    message = models.CharField(max_length=200)

    def __unicode__(self):
        return self.message


class ProfileForm(UserCreationForm):
    class Meta():
        model=Profile
        fields=['username','image']
