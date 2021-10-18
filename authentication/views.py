from django.conf import settings
from django.contrib.auth import authenticate
from django.shortcuts import redirect, render

from . import forms


def login_page(request):
    form = forms.LoginForm()
    print('debut login_page')
    if request.method == 'POST':
        print('>>>>>>>>' + request.method)
        form = forms.LoginForm(request.POST) 
        print(form.is_valid())
        if form.is_valid():
            print('fomr valid <<<<<<<<<<<<')
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            print('test')
            if user is not None:
                login(request, user)
                return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authentication/login.html', context={'form': form})







def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            User.object.create_user(request, username=username, password=password)
            print('test-2')
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authentication/signup.html', context={'form': form})


def logout_user(request):

   logout(request)

   return redirect('login')
