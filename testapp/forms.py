from django import forms
from .models import Transaction, Category, Subcategory, Type

type_choices = [(type.name, type.name) for type in Type.objects.all()]
category_choices = [(category.category, category.category) for category in Category.objects.all()]

class TransactionFilterForm(forms.Form):
    SORT_CHOICES = [
        ('type', 'По типу'),
        ('category', 'По категории'),
        ('date', 'По дате'),
        ('status', 'По статусу'),
        ('subcategory', 'По подкатегории'),
    ]
    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        widget=forms.RadioSelect,
        label='Сортировать по',
        required=False,
    )
    DATE_CHOICES = [
        ('today', 'Сегодня'),
        ('month', 'Текущий месяц'),
        ('custom', 'Период'),
    ]

    period = forms.ChoiceField(
        choices=DATE_CHOICES,
        widget=forms.RadioSelect,
        label='Период',
        required=False,
    )

    start_date = forms.DateField(
        label='С',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
    )
    end_date = forms.DateField(
        label='По',
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
    )

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['custom_date', 'amount', 'type', 'category', 'subcategory', 'status', 'comment']
        widgets = {
            'custom_date': forms.DateInput(attrs={'type': 'date'}),
            'amount': forms.NumberInput(attrs={'placeholder': 'Введите сумму транзакции'}),
            'type': forms.RadioSelect(attrs={'class': 'type-radio'}),
            'category': forms.RadioSelect(attrs={'class': 'category-radio'}),
            'subcategory': forms.RadioSelect(attrs={'class': 'subcategory-radio'}),
            'status': forms.RadioSelect(),
            'comment': forms.TextInput(attrs={'placeholder': 'Добавьте комментарий к транзакции'}),
        }