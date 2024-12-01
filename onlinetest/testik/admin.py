from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Test, Category

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    fields = ['title','slug', 'content', 'photo', 'test_photo', 'cat', 'tags']
    readonly_fields = ['test_photo']
    prepopulated_fields = {"slug": ("title", )}
    filter_horizontal = ['tags']
    list_display = ('title', 'test_photo', 'time_create', 'is_published', 'cat')
    list_display_links = ('title',)
    ordering = ['time_create', 'title']
    list_editable = ('is_published', 'cat')
    list_per_page = 10
    actions = ['set_published', 'set_draft']
    search_fields = ['title', 'cat__name']
    list_filter = ['cat__name', 'is_published']
    save_on_top = True

    @admin.display(description="Изображение", ordering='content')
    def test_photo(self, testik: Test):
        if testik.photo:
            return mark_safe(f"<img src='{testik.photo.url}' width=50>")
        return "Без фото"

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Test.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записей.")

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Test.Status.DRAFT)
        self.message_user(request, f"{count} записей сняты с публикации!", messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')