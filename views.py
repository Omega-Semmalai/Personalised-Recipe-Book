from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, viewsets
from .models import Recipe  
from .serializers import RecipeSerializer  
from rest_framework import status
import json
from django.views import View

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login

@csrf_exempt  # Use this if you're not handling CSRF tokens
def api_login_view(request):
    if request.method == 'POST':
        # Get username and password from request body
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login successful'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

    return JsonResponse({'error': 'Invalid method'}, status=405)

def login_view(request):
    return render(request, 'login.html')  # Adjust the path if necessary

@csrf_exempt  # Only use this if CSRF protection is not required
def signup_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        try:
            # Create a new user
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


from django.shortcuts import render

def home(request):
    total_recipes = Recipe.objects.count()  # Get the total count of recipes in the database
    return render(request, 'home.html', {'total_recipes': total_recipes})

def about(request):
    return render(request, 'about.html')

def upload_recipe(request):
    if request.method == 'POST':
        print(request.POST)  # Add this line to check what data is being submitted
        recipe = Recipe(
            recipe_title=request.POST['recipe_title'],
            description=request.POST['description'],
            ingredients=request.POST['ingredients'],
            instructions=request.POST['instructions']
        )
        print("Attempting to save recipe...")
        recipe.save()
        print("Recipe saved successfully!")
        
        # Check the SQL queries
        print(connection.queries)  # Add this line to log executed queries
        return redirect('view_recipe')  # Redirect to view after saving
    return render(request, 'upload_recipe.html')


def view_recipe(request):
    recipes = Recipe.objects.all()  # Get all recipes from the model
    return render(request, 'view_recipe.html', {'recipes': recipes})

def recipe_detail(request, id):
    try:
        recipe = Recipe.objects.get(id=id)
        data = {
            'recipe_title': recipe.recipe_title,
            'description': recipe.description,
            'ingredients': recipe.ingredients,
            'instructions': recipe.instructions,
        }
        return JsonResponse(data)
    except Recipe.DoesNotExist:
        return JsonResponse({'error': 'Recipe not found'}, status=404)

@csrf_exempt
def update_recipe(request, recipe_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            recipe = Recipe.objects.get(id=recipe_id)
            recipe.recipe_title = data['recipe_title']
            recipe.description = data['description']
            recipe.ingredients = data['ingredients']
            recipe.instructions = data['instructions']
            recipe.save()
            return JsonResponse({'message': 'Recipe updated successfully!'})
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
    return JsonResponse({'message': 'Invalid request method.'}, status=405)

class RecipeUpdateView(View):
    def post(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        data = json.loads(request.body)

        # Update fields
        recipe.recipe_title = data.get('recipe_title', recipe.recipe_title)
        recipe.description = data.get('description', recipe.description)
        recipe.ingredients = data.get('ingredients', recipe.ingredients)
        recipe.instructions = data.get('instructions', recipe.instructions)
        recipe.save()

        return JsonResponse({'message': 'Recipe updated successfully!'})
        
class RecipeDetail(APIView):
    def get(self, request, pk):
        try:
            recipe = Recipe.objects.get(pk=pk)
            serializer = RecipeSerializer(recipe)
            return Response(serializer.data)
        except Recipe.DoesNotExist:
            return Response({'error': 'Recipe not found'}, status=404)
        
class RecipeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def get_object(self):
        # Optional: You can add logging here to confirm the ID being fetched
        print(f"Fetching recipe with ID: {self.kwargs['pk']}")
        return super().get_object()

def delete_recipe(request, recipe_id):
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, id=recipe_id)
        recipe.delete()
        return JsonResponse({'status': 'success'}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)




class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
class RecipeDetailView(APIView):
    def get(self, request, pk):
        try:
            recipe = Recipe.objects.get(pk=pk)
            serializer = RecipeSerializer(recipe)
            return Response(serializer.data)
        except Recipe.DoesNotExist:
            return Response({'error': 'Recipe not found'}, status=status.HTTP_404_NOT_FOUND)
        
def fetch_favourites(request):
    # Fetch favourite recipes from the database
    favourites = Recipe.objects.filter(is_favourite=True)
    data = [{'id': recipe.id, 'title': recipe.recipe_title} for recipe in favourites]
    return JsonResponse(data, safe=False)

def add_to_favourites(request, recipe_id):
    if request.method == 'POST':
        try:
            recipe = Recipe.objects.get(id=recipe_id)
            recipe.is_favourite = True
            recipe.save()
            return JsonResponse({'status': 'success', 'recipe_id': recipe_id})
        except Recipe.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Recipe not found'}, status=404)


def remove_from_favourites(request, recipe_id):
    if request.method == 'POST':
        try:
            recipe = Recipe.objects.get(id=recipe_id)
            recipe.is_favourite = False
            recipe.save()
            return JsonResponse({'status': 'success', 'recipe_id': recipe_id})
        except Recipe.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Recipe not found'}, status=404)
        
