from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.contrib import messages

from . import forms

def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.add_message(request, messages.SUCCESS, 'Félicitation %s votre compte a été créé.' % user.username)
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authentication/signup.html', context={'form': form})

def logout_user(request):
   logout(request)
   return redirect('login')
