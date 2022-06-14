from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.core.exceptions import ValidationError


USER_MODEL = get_user_model()


class UserLoginForm(forms.ModelForm):

    class Meta:
        model = USER_MODEL
        fields = ('email', 'password')
        widgets = {
            'password': forms.PasswordInput()
        }

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if not (email and password):
            raise ValidationError('Необходимо заполнить поля Email и Пароль.')
        return self.cleaned_data


class UserRegistrationForm(forms.ModelForm):

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

        password_validation.validate_password(password1)

        if password1 and password2 and password1 != password2:
            raise ValidationError(
                'Два введенных пароля не совпадают.'
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
