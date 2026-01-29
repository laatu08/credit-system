from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.models import Customer, Loan
from core.serializers.create_loan import CreateLoanSerializer
from core.services.credit_engine import check_loan_eligibility
from datetime import date, timedelta


class CreateLoanView(APIView):

    def post(self, request):
        serializer = CreateLoanSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        try:
            customer = Customer.objects.get(id=data["customer_id"])
        except Customer.DoesNotExist:
            return Response(
                {"loan_approved": False, "message": "Customer not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        result = check_loan_eligibility(
            customer=customer,
            loan_amount=data["loan_amount"],
            interest_rate=data["interest_rate"],
            tenure=data["tenure"]
        )

        if not result["approval"]:
            return Response(
                {
                    "loan_id": None,
                    "customer_id": customer.id,
                    "loan_approved": False,
                    "message": "Loan not approved based on eligibility criteria",
                    "monthly_installment": round(result["monthly_installment"], 2),
                },
                status=status.HTTP_200_OK
            )

        start_date = date.today()
        end_date = start_date + timedelta(days=30 * data["tenure"])

        loan = Loan.objects.create(
            customer=customer,
            loan_amount=data["loan_amount"],
            interest_rate=result["corrected_interest_rate"],
            tenure=data["tenure"],
            monthly_installment=result["monthly_installment"],
            emis_paid_on_time=0,
            start_date=start_date,
            end_date=end_date,
        )

        return Response(
            {
                "loan_id": loan.id,
                "customer_id": customer.id,
                "loan_approved": True,
                "message": "Loan approved",
                "monthly_installment": round(loan.monthly_installment, 2),
            },
            status=status.HTTP_201_CREATED
        )
