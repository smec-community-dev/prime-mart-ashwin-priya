from django.urls import path
from .views import *

urlpatterns = [
    path('register/', seller_register, name='seller_register'),
    path('login/', seller_login, name='seller_login'),
    path('dashboard/', seller_dashboard, name='seller_dashboard'),
    path('products/', view_products, name='products'),
    path('products/add/', add_product, name='add_product'),
    path('products/update/<int:pk>/', update_product, name='update_product'),
    path('products/delete/<int:pk>/', delete_product, name='delete_product'),
    path('logout/', seller_logout, name='seller_logout'),
    path('products/image/delete/<int:pk>/', delete_product_image, name='delete_product_image'),
    path('oders/',view_orders,name='view_orders'),
    path('products/details/<int:pk>/', product_details,name='product_details')
]