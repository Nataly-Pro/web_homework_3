from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, TemplateView, UpdateView, DeleteView
from pytils.translit import slugify

from catalog.models import Product, Blog


class ProductCreateView(CreateView):
    model = Product
    fields = ('name', 'text', 'preview', 'category', 'price')
    success_url = reverse_lazy('catalog:home')


class ProductListView(ListView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Каталог'})
        return context

class ProductDetailView(DetailView):
    model = Product


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Контакты'})
        return context


class BlogListView(ListView):
    model = Blog

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'title': 'Блог'})
        return context

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'catalog/blog_detail.html'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogCreateView(CreateView):
    model = Blog
    fields = ('title', 'content', 'preview',)
    success_url = reverse_lazy('catalog:blog_list')

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()

        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'content', 'preview',)

    def form_valid(self, form):
        if form.is_valid():
            new_blog = form.save()
            new_blog.slug = slugify(new_blog.title)
            new_blog.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:blog_view', args=[self.kwargs.get('pk')])


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('catalog:blog_list')
