from rest_framework import serializers


class RegisterCustomerSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    age = serializers.IntegerField(min_value=18)
    monthly_salary = serializers.IntegerField(min_value=1)
    phone_number = serializers.IntegerField()
