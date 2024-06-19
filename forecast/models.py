from django.db import models


class Weather(models.Model):
    country = models.CharField(max_length=100)
    date = models.DateField()
    day = models.CharField(max_length=10)
    condition = models.CharField(max_length=100)
    icon = models.CharField(max_length=200)
    min_temp = models.FloatField()
    max_temp = models.FloatField()

    class Meta:
        unique_together = ('country', 'date')

    def __str__(self):
        return f"{self.country} - {self.date}"
