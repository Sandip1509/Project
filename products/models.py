from django.db import models
from django.urls import reverse
import datetime
from django.conf import settings


class EBook(models.Model):
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=500)
    publisher = models.CharField(max_length=500)
    published_date = models.DateField(default=datetime.date.today)
    genre = models.CharField(max_length=100)
    ebook_logo = models.FileField()
    bookpdf = models.FileField(blank=True, null=True)
    bookurl = models.CharField(max_length=500, default=settings.MEDIA_ROOT)
    ebook_price = models.DecimalField(max_digits=100, decimal_places=2)

    def get_absolute_url(self):
        return reverse('publisher:chapter-details', kwargs={'pk' : self.pk})

    def __str__(self):
        return self.title

    def _get_file(self):
        self._require_file()
        if not hasattr(self, '_file') or self._file is None:
            self._file = self.storage.open(self.bookpdf, 'rb')
        return self._file


class Chapter(models.Model):
    ebook = models.ForeignKey(EBook, on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    description = models.CharField(max_length=2000)
    start_page = models.IntegerField()
    end_page = models.IntegerField()
    price = models.DecimalField(max_digits=100, decimal_places=2)