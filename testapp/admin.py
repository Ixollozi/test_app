from django.contrib import admin
from testapp.models import Date, Status, Type, Category, Subcategory, Transaction

@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category', 'category_type')
    search_fields = ('category',)
    autocomplete_fields = ['category_type']


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('subcategory', 'category')
    search_fields = ('subcategory',)
    autocomplete_fields = ['category']
# Register your models here.

admin.site.register(Date)
admin.site.register(Status)
admin.site.register(Transaction)

