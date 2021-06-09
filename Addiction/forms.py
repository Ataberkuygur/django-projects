from django import forms
from .models import Addiction

class AddictionForm(forms.ModelForm):
    class Meta:
        model = Addiction
        fields = ['name']