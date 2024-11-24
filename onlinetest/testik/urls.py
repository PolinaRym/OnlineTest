from django.urls import path, re_path, register_converter
from . import views
from . import converters

register_converter(converters.FourDigitYearConverter, "year4")
urlpatterns = [
    path('', views.index, name='home'), # http://127.0.0.1.8000
    path('about/', views.about, name='about'),
    path('addpage/', views.addpage, name='add_test'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    path('test/<int:test_id>/', views.show_test, name = 'test'),
    path('category/<int:cat_id>', views.show_category, name='category')
]