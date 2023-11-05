from django.db import models

# Create your models here.
class Gallery(models.Model):
    image =  models.ImageField(upload_to='images/')
    upload_date = models.DateTimeField(auto_now_add=True)
