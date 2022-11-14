from django.db import models

# Create your models here.
class Property(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField(blank=True, null=True)
    surface = models.IntegerField(blank=True, null=True)
    full_address = models.TextField(null=True,blank=True)

    def __str__(self):
        return self.title