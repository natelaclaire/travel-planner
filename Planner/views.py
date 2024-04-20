from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

# Create your views here.
from .models import PlanType, PlanStatus, Plan, Trip, Todo, BudgetItem

def index(request):
    """View function for home page of site."""

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Generate counts of some of the main objects
    num_trips = Trip.objects.all().count()
    num_plans = Plan.objects.all().count()
    num_todos = Todo.objects.all().count()

    today = datetime.now().date()

    num_budget_items = BudgetItem.objects.all().count()
    num_past_due_todos = Todo.objects.filter(due_date__lte=today).count()
    num_past_due_budget_items = BudgetItem.objects.filter(due_date__lte=today).count()

    context = {
        'num_trips': num_trips,
        'num_plans': num_plans,
        'num_todos': num_todos,
        'num_budget_items': num_budget_items,
        'num_past_due_todos': num_past_due_todos,
        'num_past_due_budget_items': num_past_due_budget_items,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

from django.views import generic

class PlanTypeListView(generic.ListView):
    model = PlanType
    paginate_by = 10

class PlanTypeDetailView(generic.DetailView):
    model = PlanType

class PlanStatusListView(generic.ListView):
    model = PlanStatus
    paginate_by = 10

class PlanStatusDetailView(generic.DetailView):
    model = PlanStatus

class TripListView(generic.ListView):
    model = Trip
    paginate_by = 10

class TripDetailView(generic.DetailView):
    model = Trip

class PlanDetailView(generic.DetailView):
    model = Plan

class TripCreate(CreateView):
    model = Trip
    fields = '__all__'

class TripUpdate(UpdateView):
    model = Trip
    fields = '__all__'

class TripDelete(DeleteView):
    model = Trip
    success_url = reverse_lazy('trips')

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("trip-delete", kwargs={"pk": self.object.pk})
            )
