from django.shortcuts import render
from decouple import config
import openai

# Set up OpenAI API key from environment variables
openai.api_key = config('OPENAI_API_KEY')

# List of disallowed ingredients (spices, water, oil, etc.)
DISALLOWED_INGREDIENTS = ['water', 'oil', 'salt', 'pepper', 'sugar',
    'cumin', 'turmeric', 'chili', 'garam masala',
    'ginger', 'garlic', 'coriander powder', 'curry leaves',
    'bay leaves', 'cloves', 'cardamom',
    'cinnamon', 'fennel seeds', 'mustard seeds',
    'fenugreek seeds', 'black salt', 'tamarind',
    'chaat masala', 'red chili flakes',
    'lemon juice', 'lime juice',
    'paneer', 'sesame seeds', 'poppy seeds', 'potato starch', 'vinegar',
    'soya sauce', 'hot sauce', 'pickles', 'chutneys',
    'fresh herbs']

def get_recipe_suggestions(ingredients):
    # Create the prompt based on the user's input ingredients
    prompt = f"Suggest 10 recipes that can be made using the following ingredients: {', '.join(ingredients)}. " \
             f"Provide the dish name and a short description."

    # Call the OpenAI API using the new Chat API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # or "gpt-4" if you have access
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7,
    )

    # Extract suggestions from the API response
    suggestions = response['choices'][0]['message']['content'].strip().split("\n")

    # Generate Google Image Search URLs
    recipes_with_images = []
    for recipe in suggestions:
        # Cleaning up the recipe name for better Google image search
        recipe_name = recipe.strip()
        image_search_url = f"https://www.google.com/search?tbm=isch&q={'+'.join(recipe_name.split())}"

        # Append recipe name and Google Image URL
        recipes_with_images.append({
            'name': recipe_name,
            'image_link': image_search_url
        })

    return recipes_with_images

def index(request):
    suggestion_with_images = []  # Initialize empty suggestion list
    ingredient_range = range(1, 11)  # This will create a range from 1 to 10
    error_message = None  # To store validation error messages

    if request.method == 'POST':
        # Collecting ingredients from POST request
        ingredients = [
            request.POST.get(f'ingredient_{i}', '').strip().lower() for i in ingredient_range
        ]

        # Clean up empty ingredient values
        ingredients = [ing for ing in ingredients if ing]

        # Check if there's at least one valid (non-disallowed) ingredient
        valid_ingredients = [ing for ing in ingredients if ing not in DISALLOWED_INGREDIENTS]

        if not valid_ingredients:
            error_message = "Please enter at least one valid main ingredient (vegetables, meat, etc.) that is not water, oil, or spices etc."
        else:
            # If valid ingredients exist, proceed with OpenAI API call
            suggestion_with_images = get_recipe_suggestions(valid_ingredients)

    return render(request, 'index.html', {
        'suggestions': suggestion_with_images,
        'ingredient_range': ingredient_range,
        'error_message': error_message
    })
