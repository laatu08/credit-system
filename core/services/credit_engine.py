from datetime import date
from core.models import Loan


def calculate_credit_score(customer):
    loans = Loan.objects.filter(customer=customer)

    # Rule 1: If total loan amount exceeds approved limit
    total_loan_amount = sum(l.loan_amount for l in loans)
    if total_loan_amount > customer.approved_limit:
        return 0

    score = 0

    # Rule 2: EMIs paid on time (max 30)
    total_emis = sum(l.tenure for l in loans)
    emis_paid = sum(l.emis_paid_on_time for l in loans)
    if total_emis > 0:
        score += min(30, int((emis_paid / total_emis) * 30))

    # Rule 3: Number of loans (max 20)
    loan_count = loans.count()
    score += max(0, 20 - loan_count * 2)

    # Rule 4: Loan activity in current year (max 20)
    current_year = date.today().year
    active_this_year = loans.filter(start_date__year=current_year).count()
    score += min(20, active_this_year * 5)

    # Rule 5: Loan volume (max 30)
    if total_loan_amount < customer.approved_limit * 0.5:
        score += 30
    elif total_loan_amount < customer.approved_limit:
        score += 15

    return min(score, 100)


def calculate_monthly_installment(principal, annual_rate, tenure):
    r = annual_rate / (12 * 100)
    n = tenure
    return (principal * r * ((1 + r) ** n)) / (((1 + r) ** n) - 1)


def check_loan_eligibility(customer, loan_amount, interest_rate, tenure):
    score = calculate_credit_score(customer)

    corrected_rate = interest_rate
    approved = True

    if score <= 10:
        approved = False
    elif score <= 30:
        if interest_rate < 16:
            approved = False
            corrected_rate = 16
    elif score <= 50:
        if interest_rate < 12:
            approved = False
            corrected_rate = 12

    # EMI rule
    emi = calculate_monthly_installment(loan_amount, corrected_rate, tenure)
    existing_emis = sum(l.monthly_installment for l in customer.loans.all())

    if existing_emis + emi > 0.5 * customer.monthly_salary:
        approved = False

    return {
        "approval": approved,
        "credit_score": score,
        "interest_rate": interest_rate,
        "corrected_interest_rate": corrected_rate,
        "monthly_installment": emi,
    }
