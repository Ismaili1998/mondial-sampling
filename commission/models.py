from django.db import models

class AdvancePayment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.TextField(max_digits=400, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"Advance Payment {self.amount}"
