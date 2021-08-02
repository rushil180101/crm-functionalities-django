from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user', views.userPage, name='user_page'),
    path('account', views.accountSettings, name='account'),
    path('home', views.home, name='home'),
    path('register', views.registerPage, name='register'),
    path('login', views.loginPage, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('products', views.products, name='products'),
    path('customer/<str:customer_key>/', views.customer, name='customer'),
    path('create_order', views.createOrder, name='create_order'),
    path('update_order/<str:order_key>/', views.updateOrder, name='update_order'),
    path('delete_order/<str:order_key>/', views.deleteOrder, name='delete_order')
]
