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
    def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          self.fields['name'].label = "Trait"
          self.fields['image'].label = "Icon"
          self.fields['description'].label = "How to get there?"

class BadTraitForm(forms.ModelForm):
    class Meta:
        model = BadTrait
        fields = ['name', 'image', 'description']
        widgets = {
            'description': forms.Textarea()
        }
    def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)
          self.fields['name'].label = "Trait"
          self.fields['image'].label = "Icon"
          self.fields['description'].label = "How to quit?"
