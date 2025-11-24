from django.urls import path
from . import views
urlpatterns=[
    path('signup/',views.user_registration,name='user_registration'),
    path('login/',views.user_login,name="user_login"),
    path('',views.home,name='index'),
    path('logout/',views.customer_logout,name='user_logout'),
    path('product/<str:name>/', views.product_details, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist_view, name='wishlist_view'),
]