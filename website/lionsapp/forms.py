from django import forms
from django.forms import ModelForm, SelectDateWidget, EmailInput,NumberInput,Select, Textarea, FileInput
from .models import Habbit
import datetime

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Habbit
        exclude = []
        widgets = {
            'Value': Textarea(attrs={'cols': 80, 'rows': 20}),
        }
