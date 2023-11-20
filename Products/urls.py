from django.urls import path
from . import views
app_name = 'Products'
urlpatterns = [
    path('get-products/', views.getProductsByUser, name='get-products-by-user'),
    path('create-product/', views.create_product, name='create-product')
]