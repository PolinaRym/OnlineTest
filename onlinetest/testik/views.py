import self
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView
from django.views import View
from .forms import AddTestForm, UploadFileForm, ContactForm
from .models import Test, Category, TagTest, UploadFiles, Question
from .utils import DataMixin

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Создать тест", 'url_name': 'add_test'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'},
]

class TestHome(DataMixin, ListView):
    template_name = 'testik/index.html'
    context_object_name = 'tests'
    title_page = 'Главная страница'
    cat_selected = 0

    def get_queryset(self):
        return Test.published.all().select_related('cat')
@login_required
def about(request):
    test_list = Test.published.all()  # Получаем все тесты без пагинации
    return render(request, 'testik/about.html',
                  {'title': 'О сайте', 'page_obj': test_list})  # Передаем список всех тестов

class ShowTest(DataMixin, DetailView):
    template_name = 'testik/test.html'
    slug_url_kwarg = 'test_slug'
    context_object_name = 'test'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['test'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Test.published, slug=self.kwargs[self.slug_url_kwarg])


class AddTest(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddTestForm
    template_name = 'testik/addtest.html'
    title_page = 'Создание теста'

    def form_valid(self, form):
        test_instance = form.save(commit=False)
        test_instance.author = self.request.user
        test_instance.save()

        # Сохраняем вопросы и правильные ответы
        questions = self.request.POST.getlist('question[]')
        answers = self.request.POST.getlist('answer[]')

        for question, answer in zip(questions, answers):
            Question.objects.create(test=test_instance, question_text=question, correct_answer=answer)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('home')

class UpdateTest(DataMixin, UpdateView):
    model = Test
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'testik/addtest.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование теста'

class ContactFormView(LoginRequiredMixin, DataMixin, FormView):
    form_class = ContactForm
    template_name = 'testik/contact.html'
    success_url = reverse_lazy('home')
    title_page = "Обратная связь"

    def form_valid(self, form):
        print(form.cleaned_data)
        return super().form_valid(form)

def login(request):
    return HttpResponse("Авторизация")

class TestCategory(DataMixin, ListView):
    template_name = 'testik/index.html'
    context_object_name = 'tests'
    allow_empty = False

    def get_queryset(self):
        return Test.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['tests'][0].cat
        return self.get_mixin_context(context,
                                      title = 'Категория - ' + cat.name,
                                      cat_selected = cat.pk,
                                      )

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")

class TagTestList(DataMixin, ListView):
    template_name = 'testik/index.html'
    context_object_name = 'tests'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagTest.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, little='Тег: '+ tag.tag)

    def get_queryset(self):
        return Test.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

class SubmitAnswers(View):
    def post(self, request, test_slug):
        test = get_object_or_404(Test, slug=test_slug)
        user_answers = request.POST.getlist('answers[]')
        correct_answers = [question.correct_answer for question in test.questions.all()]

        score = sum(1 for user_ans, correct_ans in zip(user_answers, correct_answers) if user_ans == correct_ans)
        total_questions = len(correct_answers)

        return render(request, 'testik/results.html', {'score': score, 'total': total_questions})