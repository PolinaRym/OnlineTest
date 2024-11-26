from django.db import models
from django.urls import reverse

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Test.Status.PUBLISHED)


class Test(models.Model):
    class Status (models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name = "Заголовок")
    content = models.TextField(blank=True, verbose_name = "Тест")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name = "Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name = "Время изменения")
    is_published = models.BooleanField(choices=Status.choices,default = Status.DRAFT, verbose_name = "Статус")
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='tests', verbose_name = "Категории")
    tags = models.ManyToManyField('TagTest', blank=True, related_name = 'tags', verbose_name = "Теги")

    objects = models.Manager()
    published = PublishedManager()
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Онлайн тесты"
        verbose_name_plural = "Онлайн тесты"
        ordering = ['-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]
    def get_absolute_url(self):
        return reverse('test', kwargs={'test_slug': self.slug})

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категория"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

class TagTest(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})