from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username
    
class Recipe(models.Model):
    recipe_title = models.CharField(max_length=200)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    is_favourite = models.BooleanField(default=False)  # Add this line


    def __str__(self):
        return self.recipe_title
    
