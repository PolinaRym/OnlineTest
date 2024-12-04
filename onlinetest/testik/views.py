# views.py
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import (
    TemplateView, ListView, DetailView, FormView, CreateView, UpdateView
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import (
    HttpResponse, HttpResponseNotFound, Http404,
    HttpResponseRedirect, HttpResponsePermanentRedirect
)
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django import forms

from .forms import AddTestForm, UploadFileForm, QuestionFormSet
from .models import Test, Category, TagTest, UploadFiles
from .utils import DataMixin

# Определение меню сайта
menu = [
    {'title': "О сайте", 'url_name': 'about'},
    {'title': "Создать тест", 'url_name': 'add_test'},
    {'title': "Обратная связь", 'url_name': 'contact'},
    {'title': "Войти", 'url_name': 'login'},
]

# Главная страница с списком опубликованных тестов
class TestHome(DataMixin, ListView):
    template_name = 'testik/index.html'
    context_object_name = 'tests'
    title_page = 'Главная страница'
    cat_selected = 0

    def get_queryset(self):
        return Test.published.all().select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=self.title_page, menu=menu, cat_selected=self.cat_selected)

# Страница "О сайте" с пагинацией
@login_required
def about(request):
    contact_list = Test.published.all()
    paginator = Paginator(contact_list, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        'testik/about.html',
        {'title': 'О сайте', 'page_obj': page_obj, 'menu': menu}
    )

# Класс для отображения деталей теста и обработки ответов пользователей
class ShowTest(DataMixin, View):
    template_name = 'testik/test.html'

    def get(self, request, test_slug):
        test = get_object_or_404(Test.published, slug=test_slug)
        questions = test.questions.all()
        form = TestTakeForm(questions=questions)
        return render(
            request,
            self.template_name,
            {
                'test': test,
                'form': form,
                'menu': menu,
                'title': test.title
            }
        )

    def post(self, request, test_slug):
        test = get_object_or_404(Test.published, slug=test_slug)
        questions = test.questions.all()
        form = TestTakeForm(request.POST, questions=questions)
        if form.is_valid():
            correct = 0
            total = questions.count()
            for question in questions:
                user_answer = form.cleaned_data.get(f'question_{question.id}', '').strip().lower()
                correct_answer = question.correct_answer.strip().lower()
                if user_answer == correct_answer:
                    correct += 1
            result = f'Вы набрали {correct} из {total}'
            return render(
                request,
                'testik/test_result.html',
                {
                    'test': test,
                    'result': result,
                    'menu': menu,
                    'title': 'Результаты теста'
                }
            )
        return render(
            request,
            self.template_name,
            {
                'test': test,
                'form': form,
                'errors': form.errors,
                'menu': menu,
                'title': test.title
            }
        )

# Форма для прохождения теста
class TestTakeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super(TestTakeForm, self).__init__(*args, **kwargs)
        for question in questions:
            self.fields[f'question_{question.id}'] = forms.CharField(
                label=question.text,
                max_length=255,
                widget=forms.TextInput(attrs={'class': 'form-input'})
            )

# Класс для добавления нового теста с вопросами
class AddTest(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddTestForm
    template_name = 'testik/addtest.html'
    title_page = 'Создание теста'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = QuestionFormSet(self.request.POST)
        else:
            context['formset'] = QuestionFormSet()
        context['menu'] = menu
        context['title'] = self.title_page
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save(commit=False)
            self.object.author = self.request.user
            self.object.save()
            form.save_m2m()
            formset.instance = self.object
            formset.save()
            messages.success(self.request, "Тест успешно создан!")
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

# Класс для редактирования существующего теста
class UpdateTest(DataMixin, UpdateView):
    model = Test
    form_class = AddTestForm  # Используем ту же форму, что и для создания
    template_name = 'testik/addtest.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование теста'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = QuestionFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = QuestionFormSet(instance=self.object)
        context['menu'] = menu
        context['title'] = self.title_page
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.save()
            messages.success(self.request, "Тест успешно обновлен!")
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))

# Страница обратной связи
def contact(request):
    return render(request, 'testik/contact.html', {'title': 'Обратная связь', 'menu': menu})

# Страница авторизации
def login(request):
    return render(request, 'testik/login.html', {'title': 'Авторизация', 'menu': menu})

# Класс для отображения тестов по категории
class TestCategory(DataMixin, ListView):
    template_name = 'testik/index.html'
    context_object_name = 'tests'
    allow_empty = False

    def get_queryset(self):
        return Test.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['tests'][0].cat
        return self.get_mixin_context(
            context,
            title='Категория - ' + cat.name,
            cat_selected=cat.pk,
            menu=menu
        )

# Класс для отображения тестов по тегу
class TagTestList(DataMixin, ListView):
    template_name = 'testik/index.html'
    context_object_name = 'tests'
    allow_empty = False

    def get_queryset(self):
        return Test.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = get_object_or_404(TagTest, slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(
            context,
            title='Тег: ' + tag.tag,
            menu=menu
        )

# Обработка ошибки 404
def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")

# Дополнительные классы и функции могут быть добавлены ниже