from datetime import datetime

from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, DateInput, Select, Textarea

from Planner.models import Trip, Todo, BudgetItem


class AddTripTodoForm(ModelForm):

    class Meta:
        model = Todo
        fields = ['description', 'notes', 'trip', 'plan', 'due_date']
        widgets = {
            'description': TextInput(attrs={'class': 'form-control'}),
            'notes': Textarea(attrs={'class': 'form-control'}),
            'plan': Select(attrs={'class': 'form-select'}),
            'due_date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class AddTripBudgetItemForm(ModelForm):

    class Meta:
        model = BudgetItem
        fields = ['description', 'notes', 'trip', 'plan', 'due_date', 'amount', 'type']
        widgets = {
            'description': TextInput(attrs={'class': 'form-control'}),
            'notes': Textarea(attrs={'class': 'form-control'}),
            'plan': Select(attrs={'class': 'form-select'}),
            'due_date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'type': Select(attrs={'class': 'form-select'}),
            'amount': TextInput(attrs={'class': 'form-control'}),
        }