from django import forms
from .models import Request, Comment, ClientComment


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ["title", "description", "image", 'contact_info']
        labels = {
            "title": "Заголовок",
            "description": "Описание",
            "image": "Изображение",
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите заголовок"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Опишите свои услуги"}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]
        labels = {"text": "Комментарий"}
        widgets = {
            "text": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Оставьте комментарий"}),
        }

class ClientCommentForm(forms.ModelForm):
    class Meta:
        model = ClientComment
        fields = ['text']
        labels = {"text": "Комментарий"}
        widgets = {
            "text": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Оставьте комментарий"}),
        }


from django import forms
from .models import ClientRequest

class ClientRequestForm(forms.ModelForm):
    class Meta:
        model = ClientRequest
        fields = ["title", "description", "image", 'contact_info']