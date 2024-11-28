from django.db import models

# Create your models here.
# creates the code for making the tables


class Dreamer(models.Model):
    firstname = models.CharField(max_length = 20)
    lastname = models.CharField(max_length = 20)
    def __str__(self):
        return f'Dreamer #{self.id} Name: {self.firstname} {self.lastname}'
   
class Dream(models.Model):
    Type = [
        ('Personal', 'Personal'), 
        ('Professional', 'Professional'),
    ]

    type = models.CharField(
        max_length=50,
        choices=Type
    )

    description = models.CharField(max_length = 50)
    dreamer = models.ForeignKey(Dreamer, on_delete = models.CASCADE)
    def __str__(self):
        return f'Dreamer {self.dreamer.firstname} {self.dreamer.lastname}, Type: {self.type}, Description: {self.description}'
