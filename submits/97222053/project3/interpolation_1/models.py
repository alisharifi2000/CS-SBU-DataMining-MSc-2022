from django.db import models

class Data(models.Model):
    """
    Represents a Data
    """
    vol = models.IntegerField()


class DataSeries(models.Model):
    """
    Represents a single Buoy datapoint
    """
    data = models.ForeignKey(Data, related_name='data', on_delete=models.CASCADE)
    date = models.DateTimeField()
