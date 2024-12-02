from django.urls import path, include
from . import views 
from .views import RecipeDetailView, RecipeViewSet, RecipeDetail,recipe_detail,RecipeUpdateView,signup_view,login_view, fetch_favourites, add_to_favourites, remove_from_favourites
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet)  # This handles CRUD for recipes using the RecipeViewSet

urlpatterns = [
    path('', views.login_view, name='login'),  # Redirect root to login view
    path('api/login/', views.api_login_view, name='api_login'),  # For AJAX login
    path('signup/', signup_view, name='signup'),  # Signup page

    path('home/', views.home, name='home'),  # Home page
    path('about/', views.about, name='about'),  # About page
    path('upload/', views.upload_recipe, name='upload_recipe'),  # Upload recipe page
    path('view/', views.view_recipe, name='view_recipe'),  # View all recipes page

    path('api/recipes/<int:pk>/', RecipeDetail.as_view(), name='recipe-detail'),  # API view for individual recipe detail
    path('recipes/<int:id>/', recipe_detail, name='recipe_detail'),  # Regular view for individual recipe detail
    path('recipes/<int:recipe_id>/update/', RecipeUpdateView.as_view(), name='update_recipe'),  # Update recipe
    path('recipes/<int:recipe_id>/delete/', views.delete_recipe, name='delete_recipe'),  # Delete recipe

    path('api/', include(router.urls)),  # Include all API endpoints registered with the router

]


