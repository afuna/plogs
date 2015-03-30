from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import forms, login, authenticate
from django.http import HttpResponseRedirect

# Create your views here.
def index(request):
    return render(request, 'main/index.html')

def signup(request):
    if request.method == 'POST':
        form = forms.UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, user)

            return redirect(reverse('planes:new'))
    else:
        form = forms.UserCreationForm()

    data = {
        'form': form
    }
    return render(request, 'registration/signup.html', data)
