from datetime import datetime

from django.db.models import Sum
from django.forms import TextInput, DateInput, Textarea
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from .forms import AddTripTodoForm, AddTripBudgetItemForm, AddPlanTodoForm, AddPlanBudgetItemForm, AddTripPlanForm, \
    TripForm, UpdateTodoForm, UpdateBudgetItemForm, PlanForm, PlanStatusForm, PlanTypeForm
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
    past_due_todos = Todo.objects.filter(due_date__lte=today, date_completed__isnull=True).all()
    past_due_budget_items = BudgetItem.objects.filter(due_date__lte=today, type__in=['es','ac']).all()

    context = {
        'num_trips': num_trips,
        'num_plans': num_plans,
        'num_todos': num_todos,
        'num_budget_items': num_budget_items,
        'past_due_todos': past_due_todos,
        'past_due_budget_items': past_due_budget_items,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def settings(request):

    # Render the HTML template settings.html with the data in the context variable
    return render(request, 'settings.html')

def about(request):

    # Render the HTML template settings.html with the data in the context variable
    return render(request, 'about.html')

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
        context["planform"] = AddTripPlanForm(initial=data)
        context["budget"] = BudgetItem.objects.filter(trip=self.object).aggregate(total=Sum('amount'))
        context["budget_expended"] = BudgetItem.objects.filter(trip=self.object, type='ex').aggregate(
            total=Sum('amount'))
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

        elif request.POST.get('addtype') == "plan":
            form = AddTripPlanForm(request.POST)
            if form.is_valid():
                plan = form.save()

                return HttpResponseRedirect(reverse('trip-detail', args=[plan.trip_id]))

            else:
                self.object = self.get_object()
                context = super(self).get_context_data(**kwargs)
                context['planform'] = form
                return self.render_to_response(context=context)

        elif request.POST.get('completetodo'):
            todo = Todo.objects.get(pk=request.POST['completetodo'])
            todo.date_completed = datetime.now()
            todo.save()
            return HttpResponseRedirect(reverse('trip-detail', args=[todo.trip_id]))

class PlanDetailView(generic.DetailView):
    model = Plan

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        data = {'trip': self.object.trip, 'plan': self.object}
        context["todoform"] = AddPlanTodoForm(initial=data)
        context["budgetitemform"] = AddPlanBudgetItemForm(initial=data)
        context["budget"] = BudgetItem.objects.filter(plan=self.object).aggregate(total=Sum('amount'))
        context["budget_expended"] = BudgetItem.objects.filter(plan=self.object, type='ex').aggregate(
            total=Sum('amount'))
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('addtype')=="todo":
            form = AddPlanTodoForm(request.POST)
            if form.is_valid():
                todo = form.save()

                return HttpResponseRedirect(reverse('plan-detail', args=[todo.plan_id]))

            else:
                self.object = self.get_object()
                context = super(self).get_context_data(**kwargs)
                context['todoform'] = form
                return self.render_to_response(context=context)

        elif request.POST.get('addtype')=="budgetitem":
            form = AddPlanBudgetItemForm(request.POST)
            if form.is_valid():
                budgetitem = form.save()

                return HttpResponseRedirect(reverse('plan-detail', args=[budgetitem.plan_id]))

            else:
                self.object = self.get_object()
                context = super(self).get_context_data(**kwargs)
                context['budgetitemform'] = form
                return self.render_to_response(context=context)

        elif request.POST.get('completetodo'):
            todo = Todo.objects.get(pk=request.POST['completetodo'])
            todo.date_completed = datetime.now()
            todo.save()
            return HttpResponseRedirect(reverse('plan-detail', args=[todo.plan_id]))

class TripCreate(CreateView):
    model = Trip
    form_class = TripForm

class TripUpdate(UpdateView):
    model = Trip
    form_class = TripForm

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

class PlanUpdate(UpdateView):
    model = Plan
    form_class = PlanForm

class PlanDelete(DeleteView):
    model = Plan

    def form_valid(self, form):
        try:
            trip_id = self.object.trip.pk
            self.object.delete()
            return HttpResponseRedirect(
                reverse('trip-detail', kwargs={'pk': trip_id})
            )
        except Exception as e:
            return HttpResponseRedirect(
                reverse("plan-delete", kwargs={"pk": self.object.pk})
            )

class TodoUpdate(UpdateView):
    model = Todo
    form_class = UpdateTodoForm

    def get_success_url(self):
        if self.object.plan_id:
            return reverse('plan-detail', args=[self.object.plan_id])
        else:
            return reverse('trip-detail', args=[self.object.trip_id])

class BudgetItemUpdate(UpdateView):
    model = BudgetItem
    form_class = UpdateBudgetItemForm

    def get_success_url(self):
        if self.object.plan_id:
            return reverse('plan-detail', args=[self.object.plan_id])
        else:
            return reverse('trip-detail', args=[self.object.trip_id])

class BudgetItemDelete(DeleteView):
    model = BudgetItem

    def form_valid(self, form):
        try:
            if self.object.plan_id:
                plan_id = self.object.plan.pk
                redirect_to = reverse('plan-detail', kwargs={'pk': plan_id})
            else:
                trip_id = self.object.trip.pk
                redirect_to = reverse('trip-detail', kwargs={'pk': trip_id})

            self.object.delete()
            return HttpResponseRedirect(
                redirect_to
            )
        except Exception as e:
            return HttpResponseRedirect(
                reverse("budgetitem-delete", kwargs={"pk": self.object.pk})
            )

class TodoDelete(DeleteView):
    model = Todo

    def form_valid(self, form):
        try:
            if self.object.plan_id:
                plan_id = self.object.plan.pk
                redirect_to = reverse('plan-detail', kwargs={'pk': plan_id})
            else:
                trip_id = self.object.trip.pk
                redirect_to = reverse('trip-detail', kwargs={'pk': trip_id})

            self.object.delete()
            return HttpResponseRedirect(
                redirect_to
            )
        except Exception as e:
            return HttpResponseRedirect(
                reverse("todo-delete", kwargs={"pk": self.object.pk})
            )

class PlanStatusCreate(CreateView):
    model = PlanStatus
    form_class = PlanStatusForm
    success_url = reverse_lazy('planstatuses')

class PlanStatusUpdate(UpdateView):
    model = PlanStatus
    form_class = PlanStatusForm
    success_url = reverse_lazy('planstatuses')

class PlanTypeCreate(CreateView):
    model = PlanType
    form_class = PlanTypeForm
    success_url = reverse_lazy('plantypes')

class PlanTypeUpdate(UpdateView):
    model = PlanType
    form_class = PlanTypeForm
    success_url = reverse_lazy('plantypes')

class PlanTypeDelete(DeleteView):
    model = PlanType
    success_url = reverse_lazy('plantypes')

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("plantype-delete", kwargs={"pk": self.object.pk})
            )

class PlanStatusDelete(DeleteView):
    model = PlanStatus
    success_url = reverse_lazy('planstatuses')

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception as e:
            return HttpResponseRedirect(
                reverse("planstatus-delete", kwargs={"pk": self.object.pk})
            )