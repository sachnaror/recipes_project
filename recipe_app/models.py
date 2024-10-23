from django.db import models

class Recipe(models.Model):
    name = models.CharField(max_length=200)
    ingredients = models.TextField()
    instructions = models.TextField()
    image_url = models.URLField(blank=True)

    def __str__(self):
        return self.name
