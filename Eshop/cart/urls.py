from django.urls import path

from .views import AddToCart

from .views import view_cart, get_cart_item_count, increase_quantity,decrease_quantity,remove_item


urlpatterns =[
    path('', view_cart, name = 'view_cart'),
    path('add/', AddToCart.as_view(), name='add_to_cart'),
    path('cart/count/',get_cart_item_count, name = 'cart_count'),

    path("increase/<int:product_id>/", increase_quantity, name="increase_quantity"),
    path("decrease/<int:product_id>/", decrease_quantity, name="decrease_quantity"),
    path("remove/<int:product_id>/", remove_item, name="remove_item"),  
]