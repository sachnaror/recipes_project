from django.shortcuts import render
from django.http import JsonResponse
import openai
import json

def suggest_recipes(ingredients):
    # Replace with your OpenAI API key
    openai.api_key = 'your-api-key'

    prompt = f"""Given these Indian ingredients: {', '.join(ingredients)}
    Suggest up to 10 Indian dishes that can be made using these as main ingredients,
    along with common Indian spices and other basic ingredients.
    For each dish provide:
    1. Name (in both English and Hindi if applicable)
    2. Full ingredient list
    3. Cooking instructions
    4. A search term for finding an image
    Format as JSON."""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful Indian cooking expert."},
            {"role": "user", "content": prompt}
        ]
    )

    return json.loads(response.choices[0].message.content)

def index(request):
    if request.method == 'POST':
        ingredients = [
            request.POST.get(f'ingredient_{i}')
            for i in range(1, 11)
            if request.POST.get(f'ingredient_{i}')
        ]

        if ingredients:
            recipes = suggest_recipes(ingredients)
            return JsonResponse({'recipes': recipes})

    return render(request, 'recipe_app/index.html')
