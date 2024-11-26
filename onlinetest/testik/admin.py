from django.contrib import admin
from .models import Test, Category

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    fields = ['title','slug', 'content', 'cat', 'tags']
    prepopulated_fields = {"slug": ("title", )}
    filter_horizontal = ['tags']
    list_display = ('title', 'time_create', 'is_published', 'cat', 'brief_info')
    list_display_links = ('title',)
    ordering = ['time_create', 'title']
    list_editable = ('is_published', 'cat')
    list_per_page = 10
    actions = ['set_published', 'set_draft']
    search_fields = ['title', 'cat__name']
    list_filter = ['cat__name', 'is_published']

    @admin.display(description="Краткое описание", ordering='content')
    def brief_info(self, obj):
        return f"Описание {len(obj.content)} символов"

    def set_published(self, request, queryset):
        queryset.update(is_published=Test.Status.PUBLISHED)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')