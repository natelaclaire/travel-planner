from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('plantypes/', views.PlanTypeListView.as_view(), name='plantypes'),
    path('plantype/<int:pk>', views.PlanTypeDetailView.as_view(), name='plantype-detail'),
    path('planstatuses/', views.PlanStatusListView.as_view(), name='planstatuses'),
    path('planstatus/<int:pk>', views.PlanStatusDetailView.as_view(), name='planstatus-detail'),
    path('trips/', views.TripListView.as_view(), name='trips'),
    path('trip/<int:pk>', views.TripDetailView.as_view(), name='trip-detail'),
    path('plan/<int:pk>', views.PlanDetailView.as_view(), name='plan-detail'),
    path('trip/create/', views.TripCreate.as_view(), name='trip-create'),
    path('trip/<int:pk>/update/', views.TripUpdate.as_view(), name='trip-update'),
    path('trip/<int:pk>/delete/', views.TripDelete.as_view(), name='trip-delete'),
]
