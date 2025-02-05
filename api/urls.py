from django.urls import path, include
from .views import register_view, login_view, logout_view


urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('expenses/', include('expenses.urls')),  # Include 'expenses' URLs under 'api/expenses/'
    path('income/', include('incomes.urls')),
]