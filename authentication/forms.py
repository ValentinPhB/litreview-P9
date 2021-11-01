from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ("username",)

    def clean_password2(self):
        """Cheking if passwords are equal

        Raises:
            ValidationError: Error for user.

        Returns:
            [str]: password_2
        """
        password_1 = self.cleaned_data.get('password1')
        password_2 = self.cleaned_data.get('password2')
        if password_1 and password_2 and password_1 != password_2:
            raise ValidationError(_('Les mots de passe ne correspondent pas.'))
        return password_2
