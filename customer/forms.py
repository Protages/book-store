from django import forms
from django.contrib.auth import get_user_model


USER_MODEL = get_user_model()


class UserSettingForm(forms.ModelForm):

    class Meta:
        model = USER_MODEL
        fields = [
            'first_name', 'image', 'gender', 'birthday', 'phone', 'about', 'country'
        ]
        widgets = {
            'image': forms.FileInput(attrs={'type': 'file'})
        }
