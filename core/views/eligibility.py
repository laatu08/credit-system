from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.models import Customer
from core.serializers.eligibility import CheckEligibilitySerializer
from core.services.credit_engine import check_loan_eligibility


class CheckEligibilityView(APIView):

    def post(self, request):
        serializer = CheckEligibilitySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data
        customer_id = data["customer_id"]

        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return Response(
                {"error": "Customer not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        result = check_loan_eligibility(
            customer=customer,
            loan_amount=data["loan_amount"],
            interest_rate=data["interest_rate"],
            tenure=data["tenure"]
        )

        return Response(
            {
                "customer_id": customer.id,
                "approval": result["approval"],
                "interest_rate": result["interest_rate"],
                "corrected_interest_rate": result["corrected_interest_rate"],
                "tenure": data["tenure"],
                "monthly_installment": round(result["monthly_installment"], 2),
            },
            status=status.HTTP_200_OK
        )
