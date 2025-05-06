import datetime
from .forms import TransactionFilterForm, TransactionForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
import json

from .models import Type, Category, Subcategory, Transaction, Status, Date
from .forms import (
    TransactionForm, TypeForm, StatusForm,
    CategoryForm, SubcategoryForm
)


def home_page(request):
    form = TransactionFilterForm(request.GET or None)
    transactions = Transaction.objects.all()

    if form.is_valid():
        sort_by = form.cleaned_data.get('sort_by')
        period = form.cleaned_data.get('period')


        if sort_by == 'type':
            transactions = transactions.order_by('type__name')
        elif sort_by == 'category':
            transactions = transactions.order_by('category__category')
        elif sort_by == 'status':
            transactions = transactions.order_by('status')
        elif sort_by == 'subcategory':
            transactions = transactions.order_by('subcategory')


        elif period == 'today':
            try:
                today = datetime.date.today()
                dates = Date.objects.all().filter(date=today)
                transactions = transactions.filter(date__in=dates)
                if not transactions.exists():
                    context = {
                        'form': form,
                        'message': 'Транзакции за сегодня не найдены'
                    }
                    return render(request, 'home.html', context)
            except Exception as e:
                context = {
                    'form': form,
                    'error': str(e)
                }
                return render(request, 'home.html', context)
        elif period == 'month':
            try:
                current_month = datetime.date.today().month
                transactions = transactions.filter(created_at__month=current_month)
                transactions = transactions.order_by('created_at')
                if not transactions.exists():
                    context = {
                        'form': form,
                        'message': 'Транзакции за текущий месяц не найдены'
                    }
                    return render(request, 'home.html', context)
            except Exception as e:
                context = {
                    'form': form,
                    'error': str(e)
                }
                return render(request, 'home.html', context)
        elif period == 'custom':
            start_date = form.cleaned_data.get('start_date')
            end_date = form.cleaned_data.get('end_date')
            transactions = transactions.filter(created_at__range=[start_date, end_date])
            # фильтрация по порядку
            transactions = transactions.order_by('created_at')
            print(transactions)
            if not transactions.exists():
                context = {
                    'form': form,
                    'message': 'Транзакции за выбранный период не найдены'
                }
                return render(request, 'home.html', context)

    context = {
        'transactions': transactions,
        'form': form,
    }
    return render(request, 'home.html', context)




def create_transaction(request):
    transaction_form = TransactionForm(request.POST or None)

    if request.method == 'POST' and transaction_form.is_valid():
        transaction = transaction_form.save(commit=False)

        # Если выбрана пользовательская дата, используем её
        if transaction.custom_date:
            transaction.created_at = transaction.custom_date

        transaction.save()
        # Сигнал post_save создаст запись в модели Date
        return redirect('home')

    # Подготавливаем данные для JavaScript
    types_data = {str(t.id): t.name for t in Type.objects.all()}

    categories_data = {}
    subcategories_data = {}

    for type_obj in Type.objects.all():
        type_categories = Category.objects.filter(category_type=type_obj)
        if type_categories:
            categories_data[str(type_obj.id)] = {str(c.id): c.category for c in type_categories}

    for category in Category.objects.all():
        subcats = Subcategory.objects.filter(category=category)
        if subcats:
            subcategories_data[str(category.id)] = {str(s.id): s.subcategory for s in subcats}

    context = {
        'form': transaction_form,
        'types_json': json.dumps(types_data),
        'categories_json': json.dumps(categories_data),
        'subcategories_json': json.dumps(subcategories_data),
    }

    return render(request, 'create_transactions.html', context)


def get_categories(request):
    type_id = request.GET.get('type_id')
    if type_id:
        categories = Category.objects.filter(category_type_id=type_id)
        return JsonResponse({str(c.id): c.category for c in categories})
    return JsonResponse({})


def get_subcategories(request):
    category_id = request.GET.get('category_id')
    if category_id:
        subcategories = Subcategory.objects.filter(category=category_id)
        return JsonResponse({str(s.id): s.subcategory for s in subcategories})
    return JsonResponse({})


class ReferenceManagementView(ListView):
    template_name = 'reference_management.html'
    model = Type
    context_object_name = 'types'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses'] = Status.objects.all()
        context['categories'] = Category.objects.all()
        context['subcategories'] = Subcategory.objects.all()

        # Формы для создания новых объектов
        context['type_form'] = TypeForm()
        context['status_form'] = StatusForm()
        context['category_form'] = CategoryForm()
        context['subcategory_form'] = SubcategoryForm()

        return context


# Type CRUD
class TypeCreateView(CreateView):
    model = Type
    form_class = TypeForm
    success_url = reverse_lazy('reference_management')

    def form_valid(self, form):
        messages.success(self.request, 'Тип успешно создан')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка при создании типа')
        return redirect(self.success_url)


class TypeUpdateView(UpdateView):
    model = Type
    form_class = TypeForm
    success_url = reverse_lazy('reference_management')

    def form_valid(self, form):
        messages.success(self.request, 'Тип успешно обновлен')
        return super().form_valid(form)


class TypeDeleteView(DeleteView):
    model = Type
    success_url = reverse_lazy('reference_management')

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(request, 'Тип успешно удален')
            return response
        except Exception as e:
            messages.error(request, f'Не удалось удалить тип: {str(e)}')
            return redirect(self.success_url)


# Status CRUD
class StatusCreateView(CreateView):
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy('reference_management')

    def form_valid(self, form):
        messages.success(self.request, 'Статус успешно создан')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка при создании статуса')
        return redirect(self.success_url)


class StatusUpdateView(UpdateView):
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy('reference_management')

    def form_valid(self, form):
        messages.success(self.request, 'Статус успешно обновлен')
        return super().form_valid(form)


class StatusDeleteView(DeleteView):
    model = Status
    success_url = reverse_lazy('reference_management')

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(request, 'Статус успешно удален')
            return response
        except Exception as e:
            messages.error(request, f'Не удалось удалить статус: {str(e)}')
            return redirect(self.success_url)


# Category CRUD
class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('reference_management')

    def form_valid(self, form):
        messages.success(self.request, 'Категория успешно создана')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка при создании категории')
        return redirect(self.success_url)


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('reference_management')

    def form_valid(self, form):
        messages.success(self.request, 'Категория успешно обновлена')
        return super().form_valid(form)


class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('reference_management')

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(request, 'Категория успешно удалена')
            return response
        except Exception as e:
            messages.error(request, f'Не удалось удалить категорию: {str(e)}')
            return redirect(self.success_url)


# Subcategory CRUD
class SubcategoryCreateView(CreateView):
    model = Subcategory
    form_class = SubcategoryForm
    success_url = reverse_lazy('reference_management')

    def form_valid(self, form):
        messages.success(self.request, 'Подкатегория успешно создана')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка при создании подкатегории')
        return redirect(self.success_url)


class SubcategoryUpdateView(UpdateView):
    model = Subcategory
    form_class = SubcategoryForm
    success_url = reverse_lazy('reference_management')

    def form_valid(self, form):
        messages.success(self.request, 'Подкатегория успешно обновлена')
        return super().form_valid(form)


class SubcategoryDeleteView(DeleteView):
    model = Subcategory
    success_url = reverse_lazy('reference_management')

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(request, 'Подкатегория успешно удалена')
            return response
        except Exception as e:
            messages.error(request, f'Не удалось удалить подкатегорию: {str(e)}')
            return redirect(self.success_url)


# AJAX-запросы для динамического управления зависимостями
def get_categories_for_management(request):
    type_id = request.GET.get('type_id')
    if type_id:
        categories = Category.objects.filter(category_type_id=type_id)
        return JsonResponse([{'id': c.id, 'name': c.category} for c in categories], safe=False)
    return JsonResponse([], safe=False)