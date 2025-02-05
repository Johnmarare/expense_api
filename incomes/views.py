from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .models import UserIncome
from .serializers import IncomeSerializer


# Pagination class for income
class IncomePagination(PageNumberPagination):
    page_size = 10  # Adjust as necessary
    page_size_query_param = 'page_size'
    max_page_size = 100


# DRY mixin to filter income by authenticated user
class UserIncomeViewMixin:
    def get_queryset(self):
        return UserIncome.objects.filter(owner=self.request.user)


class IncomeListCreateView(UserIncomeViewMixin, generics.ListCreateAPIView):
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = IncomePagination  # Add pagination

    def perform_create(self, serializer):
        # Ensure the authenticated user is set as the owner of the income record
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        # Validate POST data to ensure required fields are present
        amount = request.data.get('amount')
        source = request.data.get('source')
        description = request.data.get('description')

        if not amount or not source or not description:
            return Response({'error': 'Amount, source, and description are required fields'},
                            status=400)

        return super().create(request, *args, **kwargs)


class IncomeDetailView(UserIncomeViewMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        # Optionally, add additional validation or processing here
        serializer.save(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        # Validate PUT/PATCH data to ensure required fields are provided
        amount = request.data.get('amount')
        source = request.data.get('source')
        description = request.data.get('description')

        if not amount or not source or not description:
            return Response({'error': 'Amount, source, and description are required fields'},
                            status=400)

        return super().update(request, *args, **kwargs)
