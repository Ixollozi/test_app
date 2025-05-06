import datetime
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import HttpResponse
from .models import Transaction, Category, Type, Subcategory
from .forms import TransactionFilterForm, TransactionForm
import json


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
                transactions = transactions.filter(created_at__date=today)
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