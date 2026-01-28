from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.models import Loan


class ViewLoanView(APIView):

    def get(self, request, loan_id):
        try:
            loan = Loan.objects.select_related("customer").get(id=loan_id)
        except Loan.DoesNotExist:
            return Response(
                {"error": "Loan not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        customer = loan.customer

        return Response(
            {
                "loan_id": loan.id,
                "customer": {
                    "id": customer.id,
                    "first_name": customer.first_name,
                    "last_name": customer.last_name,
                    "phone_number": customer.phone_number,
                    "age": customer.age,
                },
                "loan_amount": loan.loan_amount,
                "interest_rate": loan.interest_rate,
                "monthly_installment": round(loan.monthly_installment, 2),
                "tenure": loan.tenure,
            },
            status=status.HTTP_200_OK
        )
