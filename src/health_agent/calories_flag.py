import json
import pandas as pd
from gradio_client import Client

# Function to use Gradio client to predict and return JSON
def predict_calories(text):
    client = Client("gokaygokay/Gemma-2-llamacpp")
    result = client.predict(
        message=f"""Role:  
    You are an AI specialized in predicting or estimating the number of calories of the food items in the text. You can analyze the text to find the food items and their corresponding calorie values. You will provide the calorie values for each food item found in the text.
    Next, after that you will need to give the tag for the corresponding food, the tag will be choice of 5 tags, which are: dietarian, vegan, non vegan, not for diabetic. You will need to give the tag for each food item found in the text.
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
    {{"food_items": ["food_item1", "food_item2", "food_item3"], "total_calories": total_calories, "tags": ["tag1", "tag2", "tag3"]}}""",
            model="gemma-2-27b-it-Q5_K_M.gguf",
            system_message="You are an AI specialized in predicting number calories for Indonesian databases and language. You identify potential food items and their corresponding calorie values in the text. You will provide the calorie values for each food item found in the text.",
            max_tokens=2048,
            temperature=0.7,
            top_p=0.95,
            top_k=40,
            repeat_penalty=1.1,
            api_name="/chat"
        )
    print(f"Result: {result}")
        
    try:
        # Extract the JSON part from the result
        json_start = result.find('{')
        json_end = result.rfind('}') + 1
        json_str = result[json_start:json_end]
        print(f"JSON String: {json_str}")
        json_data = json.loads(json_str)
        return json_data
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        return None

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