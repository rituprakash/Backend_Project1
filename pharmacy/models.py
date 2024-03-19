

# Create your models here.


from django.db import models

class Medicine(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50)
    stock = models.IntegerField(default=0)


