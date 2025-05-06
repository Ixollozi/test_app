from django.urls import path
from . import views
urlpatterns = [
    path('', views.home_page, name='home'),
    path('create_transaction/', views.create_transaction, name='create_transaction'),
    path('get_categories/', views.get_categories, name='get_categories'),
    path('get_subcategories/', views.get_subcategories, name='get_subcategories'),
]