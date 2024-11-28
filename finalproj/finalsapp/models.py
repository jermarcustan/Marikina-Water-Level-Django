from django.db import models

# Create your models here.
class DateTime(models.Model):
    datetime = models.DateTimeField()

    def __str__(self):
        return f'{self.datetime}'
    
class Record(models.Model):
    RAINFALL = 'Rainfall'
    WATERLEVEL = 'Water Level'
    
    STATION_TYPES = [
        (RAINFALL, 'Rainfall'),
        (WATERLEVEL, 'Water Level')
    ]

    STO_NINO = 'Sto. Nino'
    BOSO = 'Boso-Boso'
    ARIES = 'Mt. Aries'
    CAMPANA = 'Mt. Campana'
    ORO = 'Mt. Oro'
    NANGKA = 'Nangka'

    STATION_NAMES = [
        (STO_NINO, 'Sto. Nino'),
        (BOSO, 'Boso-Boso'),
        (ARIES, 'Mt. Aries'),
        (CAMPANA, 'Mt. Campana'),
        (ORO, 'Mt. Oro'),
        (NANGKA, 'Nangka')
    ]

    source_station_type = models.CharField(max_length=20, choices=STATION_TYPES)
    source_station_name = models.CharField(max_length=20, choices=STATION_NAMES)
    value = models.DecimalField(max_digits=10, decimal_places=4)
    datetime = models.ForeignKey(DateTime, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.source_station_type} Station {self.source_station_name} recorded {self.value} of {self.source_station_type.lower()} on {self.datetime}'