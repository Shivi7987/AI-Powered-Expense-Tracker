# from django import forms
# from .models import Goal

# class GoalForm(forms.ModelForm):
#     class Meta:
#         model = Goal
#         fields = ['name', 'start_date', 'end_date', 'amount_to_save']


# class AddAmountForm(forms.Form):
#     additional_amount = forms.DecimalField(
#         label='Additional Amount to Save',
#         min_value=0,
#         max_value=9999999,
#         decimal_places=2,
#         widget=forms.NumberInput(attrs={'step': '0.01'})
#     )

from django import forms
from .models import Goal

class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        exclude = ['owner', 'current_saved_amount', 'is_achieved']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Goal Name'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'amount_to_save': forms.NumberInput(attrs={'step': '0.01'}),
        }

class AddAmountForm(forms.Form):
    additional_amount = forms.DecimalField(
        label='Additional Amount to Save',
        min_value=0,
        max_value=9999999,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01'})
    )