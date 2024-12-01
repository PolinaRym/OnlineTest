from django import template
import testik.views as views
from testik.models import Category, TagTest


register = template.Library()

@register.simple_tag()
def get_menu():
    return views.menu

@register.inclusion_tag('testik/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.all()
    return {'cats': cats, 'cat_selected': cat_selected}

@register.inclusion_tag('testik/list_tags.html')
def show_all_tags():
    return {'tags': TagTest.objects.all()}