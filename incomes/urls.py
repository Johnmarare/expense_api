from django.urls import path
from .views import IncomeListCreateView, IncomeDetailView

urlpatterns = [
    path('', IncomeListCreateView.as_view(), name='income-list'),
    path('<int:pk>/', IncomeDetailView.as_view(), name='income-detail'),
]
