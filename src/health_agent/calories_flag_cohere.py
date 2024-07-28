import os
import json
import cohere
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv(".env")

# Initialize Cohere client
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(api_key=COHERE_API_KEY)

def predict_calories(text):
    prompt = f"""Role:  
You are an AI specialized in predicting or estimating the number of calories in food items from the text. You analyze the text to find the food items and their corresponding calorie values. You provide the calorie values for each food item found in the text.
Next, you give the tag for the corresponding food, with the tags being: dietarian, vegan, non-vegan, not for diabetic. Provide the tag for each food item found in the text.
Instructions:

1. Carefully read and understand the text provided in the "Problem" section, then analyze it to predict the number of calories for each food item mentioned.
2. Identify the food items and their corresponding calorie values in the text. The food items may be mentioned with or without the calorie values.
3. List the food items and their corresponding calorie values in the specified format.
4. Sum up the total number of calories for all the food items found in the text.
5. Give the tag for each food item found in the text.

Example:
Food name: pisang goreng
ingredients: {{
    "pisang": 100,
    "tepung": 50
}}
Calories: 100 + 50 = 150
Food name: nasi goreng
ingredients: {{
    "nasi": 100,
    "minyak": 50,
    "telur": 50,
    "bawang": 20
}}
Calories: 100 + 50 + 50 + 20 = 220

Problem:  
{text}

Return the answer in this final form only (JSON):  
{{"food_items": ["food_item1", "food_item2", "food_item3"], "total_calories": total_calories, "tags": ["tag1", "tag2", "tag3"]}}"""

    try:
        response = co.generate(
            model='command-xlarge-nightly',
            prompt=prompt,
            max_tokens=2048,
            temperature=0.7,
            stop_sequences=["}"],  # To ensure it stops after generating the JSON
            return_likelihoods='NONE'
        )
        
        # Extract the generated text
        generated_text = response.generations[0].text.strip()
        
        # Extract the JSON part from the result
        json_start = generated_text.find('{')
        json_end = generated_text.rfind('}') + 1
        json_str = generated_text[json_start:json_end]
        
        # Parse the JSON string
        json_data = json.loads(json_str)
        return json_data
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage:
text = "Your text here"
result = predict_calories(text)
print(result)


# get top 5 most ordered items in data/gmr_metrics.csv
df = pd.read_csv('../../data/gmr_metrics.csv')
top5 = df['most_ordered_item'].value_counts().head(5).index.tolist()

calorie_predictions = {}

for food in top5:
    print(f"Predicting calories for {food}")
    prediction = predict_calories(food)
    if prediction:
        print(prediction)
        calorie_predictions[food] = prediction
    else:
        print(f"Failed to predict calories for {food}")

print("\nCalorie Predictions:")
print(calorie_predictions)

calorie_summary = {key: {'total_calories': value['total_calories'], 'tags': value['tags']} for key, value in calorie_predictions.items()}
print(calorie_summary)