# recipe_app/views.py

import logging
import json
from typing import List, Dict, Any
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Recipe
import openai

# Configure logging
logger = logging.getLogger(__name__)

class RecipeGenerationError(Exception):
    """Custom exception for recipe generation errors"""
    pass

def format_recipe_prompt(ingredients: List[str]) -> str:
    """Format the prompt for OpenAI API"""
    return f"""Given these Indian ingredients: {', '.join(ingredients)}
    Suggest up to 10 Indian dishes that can be made using these as main ingredients,
    along with common Indian spices and other basic ingredients.

    For each dish, provide in this exact JSON format:
    {{
        "dishes": [
            {{
                "name_english": "Dish name in English",
                "name_hindi": "Dish name in Hindi",
                "ingredients": ["ingredient1", "ingredient2", ...],
                "instructions": ["step1", "step2", ...],
                "search_term": "Search term for image",
                "cuisine_region": "Region of India this dish is from",
                "cooking_time": "Approximate cooking time",
                "difficulty": "Easy/Medium/Hard"
            }},
            ...
        ]
    }}"""

def generate_recipes(ingredients: List[str]) -> Dict[str, Any]:
    """Generate recipes using OpenAI API with error handling"""
    try:
        if not ingredients:
            raise RecipeGenerationError("No ingredients provided")

        if not settings.OPENAI_API_KEY:
            raise RecipeGenerationError("OpenAI API key not configured")

        openai.api_key = settings.OPENAI_API_KEY
        prompt = format_recipe_prompt(ingredients)

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert Indian chef who specializes in traditional recipes from all regions of India."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,  # Add some creativity but keep it reliable
            max_tokens=2000   # Ensure we get complete recipes
        )

        content = response.choices[0].message.content
        return json.loads(content)

    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {e}")
        raise RecipeGenerationError("Failed to parse recipe data")
    except openai.error.OpenAIError as e:
        logger.error(f"OpenAI API error: {e}")
        raise RecipeGenerationError("Failed to generate recipes")
    except Exception as e:
        logger.error(f"Unexpected error in recipe generation: {e}")
        raise RecipeGenerationError("An unexpected error occurred")

def index(request):
    """Main view for the recipe suggestion page"""
    try:
        if request.method == 'POST':
            # Get non-empty ingredients from the form
            ingredients = [
                ingredient.strip()
                for i in range(1, 11)
                if (ingredient := request.POST.get(f'ingredient_{i}', '').strip())
            ]

            if not ingredients:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Please provide at least one ingredient'
                }, status=400)

            recipes = generate_recipes(ingredients)

            # Save successful recipes to database (optional)
            for recipe_data in recipes.get('dishes', []):
                Recipe.objects.create(
                    name=recipe_data['name_english'],
                    ingredients='\n'.join(recipe_data['ingredients']),
                    instructions='\n'.join(recipe_data['instructions']),
                    image_url=f"https://source.unsplash.com/featured/?{recipe_data['search_term']}"
                )

            return JsonResponse({
                'status': 'success',
                'recipes': recipes
            })

        # For GET requests, render the form
        return render(request, 'recipe_app/index.html', {
            'range': range(1, 11),  # For template to iterate over input fields
            'example_ingredients': [
                'aaloo', 'pyaaz', 'tamatar', 'shimla mirch',
                'paneer', 'dal', 'bhindi', 'gobhi', 'matar', 'baigan'
            ]
        })

    except RecipeGenerationError as e:
        logger.error(f"Recipe generation error: {e}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)
    except Exception as e:
        logger.error(f"Unexpected error in index view: {e}")
        return JsonResponse({
            'status': 'error',
            'message': 'An unexpected error occurred'
        }, status=500)

@require_http_methods(["POST"])
def suggest_recipes_api(request):
    """API endpoint for recipe suggestions"""
    try:
        ingredients = request.POST.getlist('ingredients[]')
        if not ingredients:
            return JsonResponse({
                'status': 'error',
                'message': 'No ingredients provided'
            }, status=400)

        recipes = generate_recipes(ingredients)
        return JsonResponse({
            'status': 'success',
            'recipes': recipes
        })

    except RecipeGenerationError as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)
    except Exception as e:
        logger.error(f"Unexpected error in API endpoint: {e}")
        return JsonResponse({
            'status': 'error',
            'message': 'An unexpected error occurred'
        }, status=500)

def recipe_detail(request, recipe_id):
    """View for displaying individual recipe details"""
    try:
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        return render(request, 'recipe_app/recipe_detail.html', {
            'recipe': recipe,
            'ingredients_list': recipe.ingredients.split('\n'),
            'instructions_list': recipe.instructions.split('\n')
        })
    except Exception as e:
        logger.error(f"Error in recipe detail view: {e}")
        return render(request, 'recipe_app/error.html', {
            'error_message': 'Failed to load recipe details'
        })
