from django import forms
from django.forms import ModelForm, SelectDateWidget, EmailInput,NumberInput,Select, Textarea, FileInput
from .models import *
import datetime

from django import forms

class GoodTraitForm(forms.ModelForm):
    class Meta:
        model = GoodTrait
        fields = ['name', 'image', 'description']
        widgets = {
            'description': forms.Textarea()
        }
