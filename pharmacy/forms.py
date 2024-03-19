

from django import forms
from .models import Medicine


#Medicine
class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'category', 'stock']

