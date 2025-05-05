from django import forms


class TransactionFilterForm(forms.Form):
    SORT_CHOICES = [
        ('type', 'По типу'),
        ('category', 'По категории'),
        ('date', 'По дате'),

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