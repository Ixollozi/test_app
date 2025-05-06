from django import forms
from .models import Transaction, Category, Subcategory, Type, Status

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
            'amount': forms.NumberInput(attrs={'placeholder': 'Введите сумму транзакции', 'required': True}),
            'type': forms.RadioSelect(attrs={'class': 'type-radio', 'required': True}),
            'category': forms.RadioSelect(attrs={'class': 'category-radio', 'required': True}),
            'subcategory': forms.RadioSelect(attrs={'class': 'subcategory-radio', 'required': True}),
            'status': forms.RadioSelect(),
            'comment': forms.TextInput(attrs={'placeholder': 'Добавьте комментарий к транзакции'}),
        }
        error_messages = {
            'amount': {'required': 'Сумма обязательна для заполнения'},
            'type': {'required': 'Выберите тип транзакции'},
            'category': {'required': 'Выберите категорию транзакции'},
            'subcategory': {'required': 'Выберите подкатегорию транзакции'},
        }

    def clean(self):
        cleaned_data = super().clean()

        # Проверяем зависимости между полями
        type_val = cleaned_data.get('type')
        category_val = cleaned_data.get('category')

        if type_val and category_val and category_val.category_type != type_val:
            self.add_error('category', 'Категория должна соответствовать выбранному типу')

        subcategory_val = cleaned_data.get('subcategory')
        if category_val and subcategory_val and subcategory_val.category != category_val:
            self.add_error('subcategory', 'Подкатегория должна соответствовать выбранной категории')

        return cleaned_data


# Формы для управления справочниками
class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Название типа', 'required': True})
        }
        error_messages = {
            'name': {
                'required': 'Название типа обязательно',
                'unique': 'Тип с таким названием уже существует'
            }
        }


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['status']
        widgets = {
            'status': forms.TextInput(attrs={'placeholder': 'Название статуса', 'required': True})
        }
        error_messages = {
            'status': {
                'required': 'Название статуса обязательно',
                'unique': 'Статус с таким названием уже существует'
            }
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category', 'category_type']
        widgets = {
            'category': forms.TextInput(attrs={'placeholder': 'Название категории', 'required': True}),
            'category_type': forms.Select(attrs={'required': True})
        }
        error_messages = {
            'category': {
                'required': 'Название категории обязательно',
                'unique': 'Категория с таким названием уже существует'
            },
            'category_type': {'required': 'Выберите тип категории'}
        }


class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ['subcategory', 'category']
        widgets = {
            'subcategory': forms.TextInput(attrs={'placeholder': 'Название подкатегории', 'required': True}),
            'category': forms.Select(attrs={'required': True})
        }
        error_messages = {
            'subcategory': {
                'required': 'Название подкатегории обязательно',
                'unique': 'Подкатегория с таким названием уже существует'
            },
            'category': {'required': 'Выберите категорию'}
        }