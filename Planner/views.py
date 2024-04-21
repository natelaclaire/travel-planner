from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from .forms import AddTripTodoForm, AddTripBudgetItemForm
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

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        data = {'trip': self.object}
        context["todoform"] = AddTripTodoForm(initial=data)
        context["budgetitemform"] = AddTripBudgetItemForm(initial=data)
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('addtype')=="todo":
            form = AddTripTodoForm(request.POST)
            if form.is_valid():
                todo = form.save()

                return HttpResponseRedirect(reverse('trip-detail', args=[todo.trip_id]))

            else:
                self.object = self.get_object()
                context = super(self).get_context_data(**kwargs)
                context['todoform'] = form
                return self.render_to_response(context=context)

        elif request.POST.get('addtype')=="budgetitem":
            form = AddTripBudgetItemForm(request.POST)
            if form.is_valid():
                budgetitem = form.save()

                return HttpResponseRedirect(reverse('trip-detail', args=[budgetitem.trip_id]))

            else:
                self.object = self.get_object()
                context = super(self).get_context_data(**kwargs)
                context['budgetitemform'] = form
                return self.render_to_response(context=context)

        elif request.POST.get('completetodo'):
            todo = Todo.objects.get(pk=request.POST['completetodo'])
            todo.date_completed = datetime.now()
            todo.save()
            return HttpResponseRedirect(reverse('trip-detail', args=[todo.trip_id]))

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
