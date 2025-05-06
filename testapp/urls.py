from django.urls import path
from . import views

urlpatterns = [
    # Существующие URL-адреса
    path('', views.home_page, name='home'),
    path('create_transaction/', views.create_transaction),
    path('get_categories/', views.get_categories, name='get_categories'),
    path('get_subcategories/', views.get_subcategories, name='get_subcategories'),

    # URLs для управления справочниками
    path('references/', views.ReferenceManagementView.as_view(), name='reference_management'),

    # Type URLs
    path('type/create/', views.TypeCreateView.as_view(), name='type_create'),
    path('type/<int:pk>/update/', views.TypeUpdateView.as_view(), name='type_update'),
    path('type/<int:pk>/delete/', views.TypeDeleteView.as_view(), name='type_delete'),

    # Status URLs
    path('status/create/', views.StatusCreateView.as_view(), name='status_create'),
    path('status/<int:pk>/update/', views.StatusUpdateView.as_view(), name='status_update'),
    path('status/<int:pk>/delete/', views.StatusDeleteView.as_view(), name='status_delete'),

    # Category URLs
    path('category/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('category/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('category/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
    path('get_categories_for_management/', views.get_categories_for_management, name='get_categories_for_management'),

    # Subcategory URLs
    path('subcategory/create/', views.SubcategoryCreateView.as_view(), name='subcategory_create'),
    path('subcategory/<int:pk>/update/', views.SubcategoryUpdateView.as_view(), name='subcategory_update'),
    path('subcategory/<int:pk>/delete/', views.SubcategoryDeleteView.as_view(), name='subcategory_delete'),
]