from django.db import models
from django.contrib import admin

class Drinks(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.CharField(max_length=100) 
    image_url = models.URLField()  

    def __str__(self):
        return self.title


@admin.register(Drinks)
class DrinksAdmin(admin.ModelAdmin):
    pass