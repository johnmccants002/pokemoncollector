from unicodedata import name
from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_pokemon = models.CharField(max_length=50)

TYPES = (('E', 'Electric'), ('F', 'Fire'), ('R', 'Rock'), ('W', 'Water'))

# Create your models here.
class Move(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=1, choices=TYPES, default=TYPES[0][0])

    def get_absolute_url(self):
        return reverse('moves_detail', kwargs={'pk': self.id})
    
    def __str__(self):
        return self.name


class Pokemon(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    age = models.IntegerField()
    moves = models.ManyToManyField(Move)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'pokemon_id': self.id})


class Photo(models.Model):
    url = models.CharField(max_length=200)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for pokemon_id: {self.pokemon_id} @{self.url}"


class Training(models.Model):
    date = models.DateField()
    name = models.CharField(max_length= 40)

    def __str__(self):
        return f"{self.get_name_display()} on {self.date}"
    
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']