from django.urls import path

from .views import productView, searchProducts

urlpatterns = [
    path('products/', productView, name = 'products_page'),
    path('search/', searchProducts, name = 'search_products')
]

# from . import views
# urlpatterns = [
#     path('products/', views.productView, name= 'products_page'),
#     path('search/', views.searchProducts, name = 'search_products')
# ]