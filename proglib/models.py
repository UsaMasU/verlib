from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey

from django.contrib.contenttypes.fields import GenericRelation

from comment.models import Comment


class Tag(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название', unique=True)
    content = models.TextField(verbose_name='Описание', blank=True)
    slug = models.SlugField(max_length=50, verbose_name='Имя URL', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lib_tag', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Метка'
        verbose_name_plural = '3.Метки'
        ordering = ['title']


class PLC(models.Model):
    title = models.CharField(max_length=50, verbose_name='Тип', unique=True)
    content = models.TextField(verbose_name='Описание', blank=True)
    links = models.TextField(verbose_name='Ссылки', blank=True, null=True)
    slug = models.SlugField(max_length=50, verbose_name='Имя URL', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lib_plc', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Программируемый логический контроллер'
        verbose_name_plural = '4.ПЛК'
        ordering = ['title']


class HMI(models.Model):
    title = models.CharField(max_length=50, verbose_name='Тип', unique=True)
    content = models.TextField(verbose_name='Описание', blank=True)
    links = models.TextField(verbose_name='Ссылки', blank=True, null=True)
    slug = models.SlugField(max_length=50, verbose_name='Имя URL', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lib_hmi', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Человеко-машинный интерфейс'
        verbose_name_plural = '5.Визуализация'
        ordering = ['title']


class ItemAuthor(models.Model):
    name = models.CharField(max_length=50, verbose_name='Имя', unique=True)
    profile = models.TextField(verbose_name='Данные профиля', blank=True)
    slug = models.SlugField(max_length=50, verbose_name='Имя URL', unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('lib_author', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Автор модуля'
        verbose_name_plural = '6.Авторы'
        ordering = ['name']


class LibraryTree(MPTTModel):
    title = models.CharField(max_length=50, verbose_name='Название категории', unique=True)
    slug = models.SlugField(max_length=50, verbose_name='Имя URL', unique=True)
    tag = models.ManyToManyField(Tag, verbose_name="Метка", blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    photo = models.ImageField(upload_to='images/%Y/%m/%d/', verbose_name='Изображение', blank=True)
    content = models.TextField(blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('lib_category', kwargs={"slug": self.slug})

    def get_model_type(self):
        return "lib_category"

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = '1.Категории'
        ordering = ['title']

    class MPTTMeta:
        order_insertion_by = ['title']


class LibraryItem(models.Model):
    STATUS = (
        ('agreement', 'согласование'),
        ('editing', 'доработка'),
        ('actual', 'актуальный'),
        ('not_actual', 'не актуальный'),
        ('not_used', 'не используется'),
        ('operating', 'рабочий'),
        ('priority', 'приоритетный'),
    )
    title = models.CharField(verbose_name='Название', max_length=50)
    func = models.CharField(verbose_name='Функция', max_length=50)
    version = models.DecimalField(verbose_name='Версия', max_digits=10, decimal_places=2)
    category = TreeForeignKey(LibraryTree, verbose_name='Категория', on_delete=models.PROTECT)
    slug = models.SlugField(max_length=255, verbose_name='Имя URL', unique=True)
    plc = models.ManyToManyField(PLC, verbose_name="PLC", blank=True)
    hmi = models.ManyToManyField(HMI, verbose_name="HMI", blank=True)
    tag = models.ManyToManyField(Tag, verbose_name="Метка", blank=True)
    author = models.ManyToManyField(ItemAuthor, verbose_name='Автор')
    content = models.TextField(verbose_name='Описание', blank=True)
    links = models.TextField(verbose_name='Библиотека, примеры', blank=True)
    implements = models.TextField(verbose_name='Применение', blank=True)
    photo = models.ImageField(upload_to='images/%Y/%m/%d/', verbose_name='Изображение', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    comments = GenericRelation(Comment)
    status = models.CharField(max_length=30, choices=STATUS, default='agreement')

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse('lib_item', kwargs={"slug": self.slug})

    def get_model_type(self):
        return "lib_item"

    class Meta:
        verbose_name = 'Обьект'
        verbose_name_plural = '2.Обьекты'
        ordering = ['-created_at']


