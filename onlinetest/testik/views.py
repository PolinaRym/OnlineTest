from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.views import View
from django.views.generic import TemplateView

from .forms import AddTestForm, UploadFileForm
from .models import Test, Category, TagTest, UploadFiles

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Создать тест", 'url_name': 'add_test'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'},
]

def index(request):
    tests = Test.published.all().select_related('cat')
    data = {
        'title': 'Главная страница',
            'menu': menu,
            'tests': tests,
             'cat_selected': 0,
             }
    return render(request, 'testik/index.html', context=data )

class TestHome(TemplateView):
    template_name = 'testik/index.html'
    extra_context = {
        'title': 'Главная страница',
        'menu': menu,
        'tests': Test.published.all().select_related('cat'),
        'cat_selected': 0,
    }


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

def show_test(request, test_slug):
    test = get_object_or_404(Test, slug=test_slug)
    data = {
        'title': test.title,
        'menu': menu,
        'test': test,
        'cat_selected': 1,
    }
    return render(request, 'testik/test.html', data)

class AddTest(View):
    def get(self, request):
        form = AddTestForm
        data = {
            'menu': menu,
            'title': 'Создание теста',
            'form': form
        }
        return render(request, 'testik/test.html', data)

    def post(self, request):
        form = AddTestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
        data = {
            'menu': menu,
            'title': 'Создание теста',
            'form': form
        }
        return render(request, 'testik/test.html', data)



def addtest(request):
    if request.method == 'POST':
       form = AddTestForm(request.POST, request.FILES)
       if form.is_valid():
           form.save()
           return redirect('home')
    else:
        form = AddTestForm()

    data = {
        'menu': menu,
        'title': 'Добавление теста',
        'form': form

    }
    return render(request, 'testik/addtest.html', data)

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


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")

def show_tag_testlist(request, tag_slug):
    tag =  get_object_or_404(TagTest, slug=tag_slug)
    tests = tag.tags.filter(is_published=Test.Status.PUBLISHED)

    data = {
        'title': f"Тег: {tag.tag}",
        'menu': menu,
        'tests': tests,
        'cat_selected': None,
    }

    return render(request, 'testik/index.html', context=data)