from django import forms
from django.forms import ModelForm, SelectDateWidget, EmailInput,NumberInput,Select, Textarea, FileInput
from .models import Habbit
import datetime

from django import forms

class HabbitForm(forms.ModelForm):
    class Meta:
        model = Habbit
        fields = ['name', 'image', 'description']
        widgets = {
            'description': forms.Textarea()
        }
