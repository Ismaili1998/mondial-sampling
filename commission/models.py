from django.db import models
from project.models import Representative

class AdvancePayment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.TextField(max_length=400, null=True, blank=True)
    representative = models.ForeignKey(Representative,on_delete=models.CASCADE,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(null=True)

    def __str__(self):
        return str(self.amount)
    
    class Meta:
        db_table = 'advance_payment'
        ordering = ['-created_at']
