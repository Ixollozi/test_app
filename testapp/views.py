import datetime
from django.shortcuts import render
from django.http import HttpResponse
from .models import Transaction, Category
from .forms import TransactionFilterForm

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