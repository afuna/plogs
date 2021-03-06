from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import forms, login, authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .signals import post_create
from plogs.buildlogs.models import Project, BuildLog


def index(request):
    return render(request, 'main/index.html')

def signup(request):
    if request.method == 'POST':
        form = forms.UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, user)

            post_create.send(sender=User, user=user)

            return redirect(reverse('planes:new', kwargs={
                "username": user.username
            }))
    else:
        form = forms.UserCreationForm()

    data = {
        'form': form
    }
    return render(request, 'registration/signup.html', data)
