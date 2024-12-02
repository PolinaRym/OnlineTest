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

from .forms import AddTestForm, UploadFileForm
from .models import Test, Category, TagTest, UploadFiles
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
    contact_list = Test.published.all()
    paginator = Paginator(contact_list, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'testik/about.html',
                  {'title': 'О сайте', 'page_obj': page_obj})

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
        a = form.save(commit=False)
        a.author = self.request.user
        return super().form_valid(form)

class UpdateTest(DataMixin, UpdateView):
    model = Test
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'testik/addtest.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование теста'

def contact(request):
    return HttpResponse("Обратная связь")

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