from django.db import models
from django.urls import reverse
import datetime

class EBook(models.Model):
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=500)
    publisher = models.CharField(max_length=500)
    published_date = models.DateField(default=datetime.date.today)
    genre = models.CharField(max_length=100)
    ebook_logo = models.FileField()
    ebook_price = models.DecimalField(max_digits=100, decimal_places=2)

    def get_absolute_url(self):
        return reverse('publisher:detail', kwargs={'pk' : self.pk})

    def __str__(self):
        return self.title+' - '+self.genre

class Chapter(models.Model):
    ebook = models.ForeignKey(EBook, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=2000)
    price = models.DecimalField(max_digits=100, decimal_places=2)