from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, TemplateView, UpdateView, DeleteView
from pytils.translit import slugify
from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Blog, Category, Version


class CategoryListView(ListView):
    model = Category
    extra_context = {
        'title': 'Каталог товаров из Южной Кореи'
    }


class SkinProductListView(ListView):
    context_object_name = "product_list"
    queryset = Product.objects.filter(category=5)
    template_name = "/product_list.html"
    extra_context = {
        'title': 'Товары по уходу за кожей'
    }


class HygieneProductListView(ListView):
    context_object_name = "product_list"
    queryset = Product.objects.filter(category=6)
    template_name = "/product_list.html"
    extra_context = {
        'title': 'Товары личной гигиены'
    }


class HomeProductListView(ListView):
    context_object_name = "product_list"
    queryset = Product.objects.filter(category=7)
    template_name = "/product_list.html"
    extra_context = {
        'title': 'Товары для дома'
    }


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        print(self.object.pk)
        return super().form_valid(form)

    def get_success_url(self, *args, **kwargs):
        return reverse('catalog:product_view', args=[self.kwargs.get('pk')])


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)

        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
        formset.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:product_view', args=[self.kwargs.get('pk')])


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

    def get_success_url(self, *args, **kwargs):
        return reverse('catalog:blog_view', args=[self.kwargs.get('pk')])


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('catalog:blog_list')
