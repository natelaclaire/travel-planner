from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('settings/', views.settings, name='settings'),
    path('about/', views.about, name='about'),
    path('plantypes/', views.PlanTypeListView.as_view(), name='plantypes'),
    path('plantype/<int:pk>/update/', views.PlanTypeUpdate.as_view(), name='plantype-update'),
    path('plantype/<int:pk>/delete/', views.PlanTypeDelete.as_view(), name='plantype-delete'),
    path('plantype/create/', views.PlanTypeCreate.as_view(), name='plantype-create'),
    path('planstatuses/', views.PlanStatusListView.as_view(), name='planstatuses'),
    path('planstatus/<int:pk>/update/', views.PlanStatusUpdate.as_view(), name='planstatus-update'),
    path('planstatus/<int:pk>/delete/', views.PlanStatusDelete.as_view(), name='planstatus-delete'),
    path('planstatus/create/', views.PlanStatusCreate.as_view(), name='planstatus-create'),
    path('trips/', views.TripListView.as_view(), name='trips'),
    path('trip/<int:pk>', views.TripDetailView.as_view(), name='trip-detail'),
    path('plan/<int:pk>', views.PlanDetailView.as_view(), name='plan-detail'),
    path('trip/create/', views.TripCreate.as_view(), name='trip-create'),
    path('trip/<int:pk>/update/', views.TripUpdate.as_view(), name='trip-update'),
    path('trip/<int:pk>/delete/', views.TripDelete.as_view(), name='trip-delete'),
    path('plan/<int:pk>/update/', views.PlanUpdate.as_view(), name='plan-update'),
    path('plan/<int:pk>/delete/', views.PlanDelete.as_view(), name='plan-delete'),
    path('budgetitem/<int:pk>/update/', views.BudgetItemUpdate.as_view(), name='budgetitem-update'),
    path('budgetitem/<int:pk>/delete/', views.BudgetItemDelete.as_view(), name='budgetitem-delete'),
    path('todo/<int:pk>/update/', views.TodoUpdate.as_view(), name='todo-update'),
    path('todo/<int:pk>/delete/', views.TodoDelete.as_view(), name='todo-delete'),
]
