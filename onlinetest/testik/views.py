from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView

from .forms import AddTestForm, UploadFileForm
from .models import Test, Category, TagTest, UploadFiles

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Создать тест", 'url_name': 'add_test'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'},
]

class TestHome(ListView):
    template_name = 'testik/index.html'
    context_object_name = 'tests'
    extra_context = {
        'title': 'Главная страница',
        'menu': menu,
        'cat_selected': 0,
    }

    def get_queryset(self):
        return Test.published.all().select_related('cat')

def about(request):
    if request.method == 'POST':
       form = UploadFileForm(request.POST, request.FILES)
       if form.is_valid():
           fp = UploadFiles(file=form.cleaned_data['file'])
           fp.save()
    else:
       form = UploadFileForm()
    return render(request, 'testik/about.html',
                  {'title': 'О сайте','menu': menu, 'form': form})

class ShowPost(DetailView):
    # model = Women
    template_name = 'testik/test.html'
    slug_url_kwarg = 'test_slug'
    context_object_name = 'test'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['test'].title
        context['menu'] = menu
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Test.published, slug=self.kwargs[self.slug_url_kwarg])

class AddTest(FormView):
    form_class = AddTestForm
    template_name = 'testik/addtest.html'
    success_url = reverse_lazy('home')
    extra_context = {
        'menu': menu,
        'title': 'Создание теста',
    }

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

def contact(request):
    return HttpResponse("Обратная связь")

def login(request):
    return HttpResponse("Авторизация")

def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    tests = Test.published.filter(cat_id=category.pk)

    data = {
        'title': f'Категория: {category.name}',
        'menu': menu,
        'tests': tests,
        'cat_selected': category.pk,
    }
    return render(request, 'testik/index.html', context=data)

class TestCategory(ListView):
    template_name = 'testik/index.html'
    context_object_name = 'tests'
    allow_empty = False

    def get_queryset(self):
        return Test.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['tests'][0].cat
        context['title'] = 'Категория - ' + cat.name
        context['menu'] = menu
        context['cat_selected'] = cat.pk
        return context

def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")

class TagTestList(ListView):
    template_name = 'testik/index.html'
    context_object_name = 'tests'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagTest.objects.get(slug=self.kwargs['tag_slug'])
        context['title'] = 'Тег: ' + tag.tag
        context['menu'] = menu
        context['cat_selected'] = None
        return context

    def get_queryset(self):
        return Test.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')