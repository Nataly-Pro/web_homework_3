from django.db import models

import users.models


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='наименование')
    description = models.TextField(verbose_name='описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='наименование')
    text = models.TextField(verbose_name='описание')
    preview = models.ImageField(upload_to='preview/', verbose_name='изображение (превью)', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.CharField(max_length=10, verbose_name='цена за покупку')
    create_date = models.DateField(auto_now_add=True, verbose_name='дата создания')
    last_mod_date = models.DateField(auto_now=True, verbose_name='дата последнего изменения')

    owner = models.ForeignKey(users.models.User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def last_version(self):
        version = self.version_set.filter(is_actual=True).last()
        return version

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ('name',)


class Version(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    number = models.SmallIntegerField(verbose_name='номер версии')
    name = models.CharField(max_length=150, verbose_name='название версии')
    is_actual = models.BooleanField(default=False, verbose_name='признак текущей версии')

    def __str__(self):
        return f'Версия {self.number} - {self.name}'

    class Meta:
        verbose_name = 'версия'
        verbose_name_plural = 'версии'


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    slug = models.CharField(max_length=150, verbose_name='slug', null=True, blank=True)
    content = models.TextField(verbose_name='Содержимое')
    preview = models.ImageField(upload_to='blog/', verbose_name='Изображение', null=True, blank=True)
    create_date = models.DateField(auto_now=True)

    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    views_count = models.IntegerField(default=0, verbose_name='Число просмотров')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'блоговая запись'
        verbose_name_plural = 'блоговые записи'


