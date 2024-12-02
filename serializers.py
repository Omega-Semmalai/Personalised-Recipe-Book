from rest_framework import serializers
from .models import Recipe

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'recipe_title', 'description', 'ingredients', 'instructions']

    def validate_ingredients(self, value):
        if not value:  # Check if ingredients are provided
            raise serializers.ValidationError("Ingredients are required.")
        return value
