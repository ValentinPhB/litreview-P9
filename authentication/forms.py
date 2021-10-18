from authentication.models import User 
from django.forms import ModelForm, TextInput, PasswordInput, CharField, ValidationError
from django.utils.translation import gettext_lazy as _


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': TextInput(attrs={'placeholder': "Nom d'utilisateur", 'class': 'my-4 form-control'}),
            'password': PasswordInput(attrs={'placeholder': "Mot de passe", 'class': 'my-4 form-control'}),
        }
    

class SignupForm(ModelForm):
    password1 = CharField(widget=PasswordInput(attrs={'placeholder': "Mot de passe", 'class': 'my-4 form-control'}))
    password2 = CharField(widget=PasswordInput(attrs={'placeholder': "Confirmez votre mot de passe", 'class': 'my-4 form-control', 'autocomplete' : 'off'}))

    class Meta:
        model = User
        fields = ['username', 'password1','password2',]
        widgets = {
            'username': TextInput(attrs={'placeholder': "Nom d'utilisateur", 'class': 'my-4 form-control'}),
        }

    def clean_password1(self):
        cleaned_data = super(SignupForm, self).clean()
        password_1 = cleaned_data.get('password1')
        password_2 = cleaned_data.get('password2')
        if password_1 != password_2:
            raise ValidationError(_('Les mots de passe ne correspondent pas.'))
        return password_2
