from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='наименование')
    text = models.TextField(verbose_name='описание')
    preview = models.ImageField(upload_to='preview/', verbose_name='изображение (превью)', blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    price = models.CharField(max_length=10, verbose_name='цена за покупку')
    create_date = models.DateField(auto_now_add=True, verbose_name='дата создания')
    last_mod_date = models.DateField(auto_now=True, verbose_name='дата последнего изменения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ('name',)


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='наименование')
    description = models.TextField(verbose_name='описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
