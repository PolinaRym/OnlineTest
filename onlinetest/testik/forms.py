from django import forms
from .models import Category

class AddTestForm(forms.Form):
    title = forms.CharField(max_length = 255, label="Заголовок")
    slug = forms.SlugField(max_length = 255, label="URL")
    content = forms.CharField(widget=forms.Textarea(), required=False, label="Контент")
    is_published = forms.BooleanField(required=False, label="Статус")
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label="Категории")