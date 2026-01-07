from django.urls import path

from . import views

urlpatterns = [
    path('all/', views.productView, name = 'products_page')

]