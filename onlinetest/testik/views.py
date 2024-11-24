from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify

from .models import Test

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Создать тест", 'url_name': 'add_test'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'},
        ]

data_db = [
    {'id': 1, 'title': 'Схемотехника РК3', 'content': '''<h1>Асинхронные счетчики</h1>Рубежный контроль по схемотехнике — это тестирование, направленное на оценку знаний и навыков студентов в области проектирования и анализа электрических схем. 
    В ходе контроля студенты проверяют усвоение ключевых понятий, таких как законы Ома и Кирхгофа, анализ электрических цепей, а также знакомство с элементами схем, такими как резисторы, конденсаторы и индуктивности''',
     'is_published': True},
    {'id': 2, 'title': 'ОС РК2', 'content': 'Linux', 'is_published': False},
    {'id': 3, 'title': 'ССРПО ДЗ', 'content': 'Шаблон стороитель', 'is_published': True},
]

cats_db = [
    {'id': 1, 'name': 'Тесты подтверждения квалификации'},
    {'id': 2, 'name': 'Тесты повышения квалификации'},
    {'id': 3, 'name': 'Тесты на оценку технических навыков'}

]
def index(request):#HttpRequest
    data = {
        'title': 'Главная страница',
            'menu': menu,
            'tests': data_db,
             'cat_selected': 0,
             }
    return render(request, 'testik/index.html', context=data )


def about(request):
    return render(request, 'testik/about.html', {'title': 'О сайте','menu': menu})

def show_test(request, test_slug):
    test = get_object_or_404(Test, slug=test_slug)
    data = {
        'title': test.title,
        'menu': menu,
        'test': test,
        'cat_selected': 1,
    }
    return render(request, 'testik/test.html', data)


def addpage(request):
    return HttpResponse("Создать тест")

def contact(request):
    return HttpResponse("Обратная связь")

def login(request):
    return HttpResponse("Авторизация")

def show_category(request, cat_id):
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'tests': data_db,
        'cat_selected': cat_id,
    }
    return render(request, 'testik/index.html', context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
