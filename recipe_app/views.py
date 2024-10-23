import openai
from django.shortcuts import render

# Set your OpenAI API key here
openai.api_key = 'your_openai_api_key'

def index(request):
    suggestions = []

    if request.method == 'POST':
        ingredients = [
            request.POST.get('ingredient_1', ''),
            request.POST.get('ingredient_2', ''),
            request.POST.get('ingredient_3', ''),
            request.POST.get('ingredient_4', ''),
            request.POST.get('ingredient_5', ''),
            request.POST.get('ingredient_6', ''),
            request.POST.get('ingredient_7', ''),
            request.POST.get('ingredient_8', ''),
            request.POST.get('ingredient_9', ''),
            request.POST.get('ingredient_10', '')
        ]

        # Clean up the list and remove empty values
        ingredients = [ing for ing in ingredients if ing]

        # Prepare the prompt for OpenAI
        prompt = f"Suggest 10 Indian recipes that can be made using the following ingredients: {', '.join(ingredients)}. " \
                 f"Provide the dish name and short description."

        # Call GPT API
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )

        # Process the response and split it into suggestions
        suggestions = response.choices[0].text.strip().split("\n")

    return render(request, 'index.html', {'suggestions': suggestions})
