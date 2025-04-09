from django.db import models

# Create your models here.
class Library(models.Model):
    name = models.CharField(max_length=100)
    Class = models.CharField(max_length=100)
    book_id = models.CharField(max_length=20, unique=True)
    book_name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    publication = models.CharField(max_length=50)
    quantity = models.IntegerField()
    
    
    
    def __str__(self):
        return self.name