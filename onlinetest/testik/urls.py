from django.urls import path, re_path, register_converter
from . import views
from . import converters

register_converter(converters.FourDigitYearConverter, "year4")
urlpatterns = [
    path('', views.TestHome.as_view(), name='home'), # http://127.0.0.1.8000
    path('about/', views.about, name='about'),
    path('addtest/', views.AddTest.as_view(), name='add_test'),
    path('contact/', views.ContactFormView.as_view(), name='contact'),
    path('login/', views.login, name='login'),
    path('test/<slug:test_slug>/', views.ShowTest.as_view(), name = 'test'),
    path('category/<slug:cat_slug>', views.TestCategory.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.TagTestList.as_view(), name='tag'),
    path('edit/<slug:slug>/', views.UpdateTest.as_view(), name='edit_test'),

]