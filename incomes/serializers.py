from rest_framework import serializers
from .models import UserIncome

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserIncome
        fields = '__all__'
        read_only_fields = ['owner']
