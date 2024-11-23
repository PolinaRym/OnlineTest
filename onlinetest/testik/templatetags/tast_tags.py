from django import template
import testik.views as views

register = template.Library()

@register.simple_tag(name='getcats')
def get_categories():
    return views.cats_db
@register.inclusion_tag('testik/list_categories.html')
def show_categories(cat_selected):
    cats = views.cats_db
    return {'cats': cats, 'cat_selected': cat_selected}