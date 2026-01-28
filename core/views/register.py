from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.models import Customer
from core.serializers.register import RegisterCustomerSerializer


class RegisterCustomerView(APIView):

    def post(self, request):
        serializer = RegisterCustomerSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data

        approved_limit = 36 * data["monthly_salary"]

        customer = Customer.objects.create(
            external_customer_id=None,
            first_name=data["first_name"],
            last_name=data["last_name"],
            age=data["age"],
            monthly_salary=data["monthly_salary"],
            approved_limit=approved_limit,
            phone_number=data.get("phone_number"),
            current_debt=0,
        )

        return Response(
            {
                "customer_id": customer.id,
                "name": customer.first_name+" "+customer.last_name,
                "age":customer.age,
                "monthly_income": customer.monthly_salary,
                "approved_limit": approved_limit,
                "phone_number": customer.phone_number
            },
            status=status.HTTP_201_CREATED
        )
