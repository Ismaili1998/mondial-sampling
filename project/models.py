from django.db import models
from client.models import Client

class Project(models.Model):
    project_name = models.CharField(max_length=255)
    project_nbr = models.CharField(max_length=50, unique=True)
    client = models.ForeignKey(Client,on_delete=models.PROTECT)
    client_ref = models.CharField(max_length=255)
    our_ref = models.CharField(max_length=255)
    project_description = models.TextField()
    to_do = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'project'

    def __str__(self):
        return self.project_name
