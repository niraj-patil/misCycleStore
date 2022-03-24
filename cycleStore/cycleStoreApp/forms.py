
from django.core import validators
from .models import Finances
from django import forms

class FinanceForm(forms.ModelForm):
    class Meta:
        model=Finances
        fields=['id','description','type','amount','completed']
        widgets={
            'description':forms.TextInput(attrs={'class':'form-control'}),
            'type':forms.Select(attrs={'class':'form-control'}),
            'amount':forms.NumberInput(attrs={'class':'form-control'}),
            #'completed':forms.NullBooleanSelect()
            
        }
        
 