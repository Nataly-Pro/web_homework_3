from django.urls import path
from django.views.decorators.cache import cache_page, never_cache

from catalog.apps import MainConfig
from catalog.views import ProductCreateView, ProductDetailView, ContactsView, BlogCreateView, \
    BlogListView, BlogUpdateView, BlogDeleteView, BlogDetailView, CategoryListView, ProductUpdateView, \
    HygieneProductListView, SkinProductListView, HomeProductListView

app_name = MainConfig.name

urlpatterns = [
    path('', CategoryListView.as_view(), name='home'),
    path('products/?category=5', SkinProductListView.as_view(), name='skin_products'),
    path('products/?category=6', HygieneProductListView.as_view(), name='hygiene_products'),
    path('products/?category=7', HomeProductListView.as_view(), name='home_products'),
    path('create_product/', ProductCreateView.as_view(), name='create_product'),
    path('update_product/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),
    path('product/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product_view'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('blog_create/', BlogCreateView.as_view(), name='blog_create'),
    path('blog_list/', BlogListView.as_view(), name='blog_list'),
    path('blog_detail/<int:pk>/', BlogDetailView.as_view(), name='blog_view'),
    path('blog_edit/<int:pk>/', BlogUpdateView.as_view(), name='blog_edit'),
    path('blog_delete/<int:pk>/', BlogDeleteView.as_view(), name='blog_delete'),
]

