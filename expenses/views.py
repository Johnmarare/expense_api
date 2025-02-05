from rest_framework import generics, permissions
from .models import Expense
from .serializers import ExpenseSerializer

class ExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(owner=self.request.user)  # Use 'owner' here

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  # Save the authenticated user as the owner

class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(owner=self.request.user)  # Use 'owner' here
