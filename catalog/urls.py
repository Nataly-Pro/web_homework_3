from django.urls import path

from catalog.apps import MainConfig
from catalog.views import ProductCreateView, ProductListView, ProductDetailView, ContactsView, BlogCreateView, \
    BlogListView, BlogUpdateView, BlogDeleteView, BlogDetailView

app_name = MainConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('create_product/', ProductCreateView.as_view(), name='create_product'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product'),
    path('blog_create/', BlogCreateView.as_view(), name='blog_create'),
    path('blog_list/', BlogListView.as_view(), name='blog_list'),
    path('blog_detail/<int:pk>/', BlogDetailView.as_view(), name='blog_view'),
    path('blog_edit/<int:pk>/', BlogUpdateView.as_view(), name='blog_edit'),
    path('blog_delete/<int:pk>/', BlogDeleteView.as_view(), name='blog_delete'),
]

