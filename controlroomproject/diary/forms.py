from django import forms
from .models import DiaryEntry


class DiaryEntryForm(forms.ModelForm):
    class Meta:
        model = DiaryEntry
        fields = ["date", "title", "content"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }
