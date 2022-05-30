from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


USER_MODEL = get_user_model()


class UserLoginForm(forms.ModelForm):

    def clean(self):
        return self.cleaned_data

    class Meta:
        model = USER_MODEL
        fields = ('email', 'password')
        widgets = {
            'password': forms.PasswordInput()
        }


class UserRegistrationForm(forms.ModelForm):
    # error_messages = {
    #     "password_mismatch": "The two password fields didn’t match.",
    # }

    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'})
    )
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'})
    )

    class Meta:
        model = USER_MODEL
        fields = ('email', 'user_name')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            print('invalid password (from form.py)')
            raise ValidationError(
                'Два введенных пароля не совпадают.',
                code="password_mismatch",
            )
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))
        user.is_active = True
        user.first_name = self.cleaned_data.get('user_name')
        if commit:
            user.save()
        return user
