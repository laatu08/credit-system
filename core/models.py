from django.db import models

# Create your models here.
class Customer(models.Model):
    external_customer_id = models.BigIntegerField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.BigIntegerField(null=True, blank=True)
    age = models.IntegerField()
    monthly_salary = models.BigIntegerField()
    approved_limit = models.BigIntegerField()
    current_debt = models.FloatField(default=0)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Loan(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="loans"
    )
    loan_amount = models.FloatField()
    interest_rate = models.FloatField()
    tenure = models.IntegerField()  # months
    monthly_installment = models.FloatField()
    emis_paid_on_time = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Loan {self.id} - Customer {self.customer_id}"