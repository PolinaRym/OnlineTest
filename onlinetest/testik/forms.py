from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from .models import Category, Test, Question



class AddTestForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label="Категории")
    class Meta:
        model = Test
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'class': 50, 'rows': 5}),
        }
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError("Длина превышает 50 символов")

        return title

class UploadFileForm(forms.Form):
    file = forms.FileField(label = "Файл")

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'correct_answer', 'order']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-input'}),
            'correct_answer': forms.TextInput(attrs={'class': 'form-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-input'}),
        }

QuestionFormSet = inlineformset_factory(Test, Question, form=QuestionForm, extra=1, can_delete=True)