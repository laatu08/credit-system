from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core.models import Customer, Loan
from datetime import date


class ViewLoansByCustomerView(APIView):

    def get(self, request, customer_id):
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return Response(
                {"error": "Customer not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        loans = Loan.objects.filter(customer=customer)

        today = date.today()
        response = []

        for loan in loans:
            months_elapsed = (
                (today.year - loan.start_date.year) * 12
                + (today.month - loan.start_date.month)
            )
            repayments_left = max(loan.tenure - months_elapsed, 0)

            response.append(
                {
                    "loan_id": loan.id,
                    "loan_amount": loan.loan_amount,
                    "interest_rate": loan.interest_rate,
                    "monthly_installment": round(loan.monthly_installment, 2),
                    "repayments_left": repayments_left,
                }
            )

        return Response(response, status=status.HTTP_200_OK)
