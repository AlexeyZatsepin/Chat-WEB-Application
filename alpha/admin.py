from django.contrib import admin
from .models import Chat,Profile
from django.contrib.auth.models import User

admin.site.register(Chat)
#admin.site.unregister(Group)
#admin.site.unregister(User)
admin.site.register(Profile)
