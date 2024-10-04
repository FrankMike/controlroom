from django import forms
from .models import DiaryEntry, Transaction


class DiaryEntryForm(forms.ModelForm):
    class Meta:
        model = DiaryEntry
        fields = ["date", "title", "content"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            "description",
            "amount",
            "transaction_type",
            "date",
        ]
