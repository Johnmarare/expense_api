from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import Expense
from .serializers import ExpenseSerializer


# Pagination class
class ExpensePagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 50


# DRY mixin to filter expenses by authenticated user
class UserExpenseViewMixin:
    def get_queryset(self):
        return Expense.objects.filter(owner=self.request.user)


class ExpenseListCreateView(UserExpenseViewMixin, generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = ExpensePagination  # Add pagination

    def perform_create(self, serializer):
        # Ensure the authenticated user is set as the owner of the expense
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        # Validate POST data to ensure required fields are present
        amount = request.data.get('amount')
        category = request.data.get('category')
        description = request.data.get('description')

        if not amount or not category or not description:
            return Response({'error': 'Amount, category, and description are required fields'},
                            status=400)

        return super().create(request, *args, **kwargs)


class ExpenseDetailView(UserExpenseViewMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        # Optionally, I could add additional validation or processing here
        serializer.save(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        # Validate PUT/PATCH data to ensure required fields are provided
        amount = request.data.get('amount')
        category = request.data.get('category')
        description = request.data.get('description')

        if not amount or not category or not description:
            return Response({'error': 'Amount, category, and description are required fields'},
                            status=400)

        return super().update(request, *args, **kwargs)

