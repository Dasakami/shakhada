from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Review, Feedback
from django.contrib.auth.forms import (AuthenticationForm,
                                       UserCreationForm, UserChangeForm)

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите имя пользователя'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите пароль'}))

    class Meta:
        model = User
        fields = ('username', 'password')


from django import forms
from .models import Work

class WorkForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = ['title', 'description', 'image', 'video']

    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get("image")
        video = cleaned_data.get("video")

        if image and video:
            raise forms.ValidationError("Можно загрузить либо фото, либо видео, но не оба сразу.")

        if not image and not video:
            raise forms.ValidationError("Необходимо загрузить хотя бы одно медиа: фото или видео.")

        return cleaned_data

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['feedback_type', 'message']
        widgets = {
            'feedback_type': forms.Select(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите ваше сообщение'}),
        }

class UserProfileForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': True}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': True}))
    banner = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False)
    about = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}), required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image', 'username', 'email', 'image', 'banner', 'about')


class UserEmailChangeForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите новый email'
    }))

    class Meta:
        model = User
        fields = ['email']

class UserUsernameChangeForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4',
        'placeholder': 'Введите новый username'
    }))

    class Meta:
        model = User
        fields = ['username']
