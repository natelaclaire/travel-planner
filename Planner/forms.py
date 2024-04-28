from datetime import datetime

from django.core.exceptions import ValidationError
from django.forms import ModelForm, TextInput, DateInput, Select, Textarea, DateTimeInput, SplitDateTimeWidget

from Planner.models import Trip, Todo, BudgetItem, Plan, PlanStatus, PlanType


class AddTripPlanForm(ModelForm):

    class Meta:
        model = Plan
        fields = ['description', 'notes', 'trip', 'type', 'status', 'scheduled_start_date_time', 'scheduled_end_date_time']
        widgets = {
            'description': TextInput(attrs={'class': 'form-control'}),
            'notes': Textarea(attrs={'class': 'form-control', 'rows': 1}),
            'type': Select(attrs={'class': 'form-select'}),
            'status': Select(attrs={'class': 'form-select'}),
            'scheduled_start_date_time': DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'scheduled_end_date_time': DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

class AddTripTodoForm(ModelForm):

    class Meta:
        model = Todo
        fields = ['description', 'notes', 'trip', 'plan', 'due_date']
        widgets = {
            'description': TextInput(attrs={'class': 'form-control'}),
            'notes': Textarea(attrs={'class': 'form-control', 'rows': 1}),
            'plan': Select(attrs={'class': 'form-select'}),
            'due_date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class AddTripBudgetItemForm(ModelForm):

    class Meta:
        model = BudgetItem
        fields = ['description', 'notes', 'trip', 'plan', 'due_date', 'amount', 'type']
        widgets = {
            'description': TextInput(attrs={'class': 'form-control'}),
            'notes': Textarea(attrs={'class': 'form-control', 'rows': 1}),
            'plan': Select(attrs={'class': 'form-select'}),
            'due_date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'type': Select(attrs={'class': 'form-select'}),
            'amount': TextInput(attrs={'class': 'form-control'}),
        }

class AddPlanTodoForm(ModelForm):

    class Meta:
        model = Todo
        fields = ['description', 'notes', 'trip', 'plan', 'due_date']
        widgets = {
            'description': TextInput(attrs={'class': 'form-control'}),
            'notes': Textarea(attrs={'class': 'form-control', 'rows': 1}),
            'due_date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class AddPlanBudgetItemForm(ModelForm):

    class Meta:
        model = BudgetItem
        fields = ['description', 'notes', 'trip', 'plan', 'due_date', 'amount', 'type']
        widgets = {
            'description': TextInput(attrs={'class': 'form-control'}),
            'notes': Textarea(attrs={'class': 'form-control', 'rows': 1}),
            'due_date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'type': Select(attrs={'class': 'form-select'}),
            'amount': TextInput(attrs={'class': 'form-control'}),
        }

class TripForm(ModelForm):
    class Meta:
        model = Trip
        fields = '__all__'
        widgets = {
            'destination': TextInput(attrs={'class': 'form-control'}),
            'goal_date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'completed_date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': Textarea(attrs={'class': 'form-control'}),
        }

class PlanForm(ModelForm):
    class Meta:
        model = Plan
        fields = ['description', 'notes', 'type', 'status', 'scheduled_start_date_time', 'scheduled_end_date_time']
        widgets = {
            'description': TextInput(attrs={'class': 'form-control'}),
            'notes': Textarea(attrs={'class': 'form-control'}),
            'type': Select(attrs={'class': 'form-select'}),
            'status': Select(attrs={'class': 'form-select'}),
            'scheduled_start_date_time': DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'scheduled_end_date_time': DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

class UpdateBudgetItemForm(ModelForm):

    class Meta:
        model = BudgetItem
        fields = ['description', 'notes', 'due_date', 'amount', 'type']
        widgets = {
            'description': TextInput(attrs={'class': 'form-control'}),
            'notes': Textarea(attrs={'class': 'form-control'}),
            'due_date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'type': Select(attrs={'class': 'form-select'}),
            'amount': TextInput(attrs={'class': 'form-control'}),
        }

class UpdateTodoForm(ModelForm):

    class Meta:
        model = Todo
        fields = ['description', 'notes', 'due_date', 'date_completed']
        widgets = {
            'description': TextInput(attrs={'class': 'form-control'}),
            'notes': Textarea(attrs={'class': 'form-control', 'rows': 1}),
            'due_date': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_completed': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class PlanStatusForm(ModelForm):

    class Meta:
        model = PlanStatus
        fields = ['name']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
        }

class PlanTypeForm(ModelForm):

    class Meta:
        model = PlanType
        fields = ['name']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
        }