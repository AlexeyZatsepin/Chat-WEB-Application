from django.shortcuts import render
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from chat_app import settings
from django.contrib.auth.decorators import login_required
from .models import Chat, ProfileForm, Profile
from django.core.context_processors import csrf
from django.contrib import auth
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.models import User

def Login(request):
    next = request.GET.get('next', '/home/')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(next)
            else:
                return HttpResponse("Account is not active at the moment.")
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)
    return render(request, "alpha/login.html", {'next': next})


def Logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def index(request):
    return HttpResponseRedirect('/home/')


@login_required
def Home(request):
    chat = Chat.objects.raw('SELECT alpha_chat.id,message,auth_user.id as user_id,image,username FROM alpha_profile,auth_user,alpha_chat WHERE alpha_profile.user_ptr_id=auth_user.id AND alpha_chat.user_id=auth_user.id')
    id = request.user.id
    user = Profile.objects.get(id=id)
    all = list(User.objects.raw('SELECT id,image,username FROM alpha_profile,auth_user WHERE alpha_profile.user_ptr_id=auth_user.id'))
    return render(request, "alpha/home.html", {'home': 'active', 'chat': chat, 'user': user, 'all': all})


def Post(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)
        c = Chat(user=request.user, message=msg)
        if msg != '':
            c.save()
        return JsonResponse({'msg': msg, 'user': c.user.username})
    else:
        return HttpResponse('Request must be POST.')


def Messages(request):
    c = Chat.objects.raw('SELECT alpha_chat.id,message,auth_user.id as user_id,image,username FROM alpha_profile,auth_user,alpha_chat WHERE alpha_profile.user_ptr_id=auth_user.id AND alpha_chat.user_id=auth_user.id')
    id = request.user.id
    user = Profile.objects.get(id=id)
    all = list(User.objects.raw('SELECT id,image,username FROM alpha_profile,auth_user WHERE alpha_profile.user_ptr_id=auth_user.id'))
    return render(request, 'alpha/messages.html', {'chat': c,'user': user, 'all': all})


def register(request):
    args = {}
    args.update(csrf(request))
    args['form'] = ProfileForm()
    if request.POST:
        newuser_form = ProfileForm(request.POST, request.FILES)
        print("1")
        if newuser_form.is_valid():
            newuser_form.save()
            print("2")
            newuser = auth.authenticate(username=newuser_form.cleaned_data['username'],
                                        password=newuser_form.cleaned_data['password2'])
            auth.login(request, newuser)
            return redirect('/')
        else:
            args['form'] = newuser_form
    return render_to_response('alpha/register.html', args)
