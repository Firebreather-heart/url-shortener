from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Metrics(models.Model):
    visits = models.PositiveIntegerField(default=0)
    
    def new_visit(self):
        self.visits += 1
        return self

class UrlHolder(models.Model):
    destination = models.URLField(max_length=200, db_index=True, null = False, blank = False)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='urls')
    custom_addr = models.CharField(max_length=10,unique=True)
    metrics = models.ForeignKey(Metrics, on_delete=models.CASCADE, related_name='metrics', auto_created=True)

    def __str__(self) -> str:
        return "Url"


