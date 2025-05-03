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