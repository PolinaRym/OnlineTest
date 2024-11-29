from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.deconstruct import deconstructible

from .models import Category


class AddTestForm(forms.Form):
    title = forms.CharField(max_length = 255, min_length=5,
                            label="Заголовок",
                            widget=forms.TextInput(attrs={'class': 'form-input'}))
    slug = forms.SlugField(max_length = 255, label="URL",
                           validators=[
                               MinLengthValidator(5, message="Минимум 5 символов"),
                               MaxLengthValidator(100, message="Минимум 100 символов"),
                           ])
    content = forms.CharField(widget=forms.Textarea(), required=False, label="Контент")
    is_published = forms.BooleanField(required=False, initial = True, label="Статус")
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label="Категории")