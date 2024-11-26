from tabnanny import verbose

from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Test.Status.PUBLISHED)
def translit_to_eng(s: str) -> str:
     d = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g',
        'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh',
        'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k',
        'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
        'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
        'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts',
        'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': '',
        'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G',
        'Д': 'D', 'Е': 'E', 'Ё': 'Yo', 'Ж': 'Zh',
        'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K',
        'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O',
        'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T',
        'У': 'U', 'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts',
        'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch', 'Ъ': '',
        'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya',
    }
     return "".join(map(lambda x: d[x] if d.get(x, False) else x, s.lower()))

class Test(models.Model):
    class Status (models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255, verbose_name = "Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name = "Слаг")
    content = models.TextField(blank=True, verbose_name = "Тест")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name = "Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name = "Время изменения")
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                                     default = Status.DRAFT, verbose_name = "Статус")
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

    #def save(self, *args, **kwargs):
       # self.slug = slugify(translit_to_eng(self.title))
       # super().save(*args, **kwargs)

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name = "Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name = "Слаг")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категория"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

class TagTest(models.Model):
    tag = models.CharField(max_length=100, db_index=True, verbose_name = "Тег")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name = "Слаг")

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})
