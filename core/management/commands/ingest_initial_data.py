from django.core.management.base import BaseCommand
from core.tasks.ingest_data import ingest_customers, ingest_loans


class Command(BaseCommand):
    help = "Ingest initial customer and loan data using Celery"

    def handle(self, *args, **options):
        self.stdout.write("Submitting background ingestion jobs...")

        ingest_customers.delay("customer_data.xlsx")
        ingest_loans.delay("loan_data.xlsx")

        self.stdout.write(
            self.style.SUCCESS(
                "Ingestion tasks submitted successfully"
            )
        )
