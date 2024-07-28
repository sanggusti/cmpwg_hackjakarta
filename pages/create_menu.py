import streamlit as st
import cohere
from dotenv import load_dotenv
import os
import json
import re

# Load environment variables
load_dotenv(".env")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(api_key=COHERE_API_KEY)

# Page configuration
st.set_page_config(
    page_title="Create Menu",
    page_icon="🍛"
)

# Initialize session state if it doesn't exist
if 'menu_items' not in st.session_state:
    st.session_state['menu_items'] = []
if 'current_ingredients' not in st.session_state:
    st.session_state['current_ingredients'] = []
if 'tag_options' not in st.session_state:
    st.session_state['tag_options'] = ["Vegan", "Vegetarian", "Gluten-Free", "Spicy", "Nut-Free", "Bakso", "Sapi", "Mie"]
if 'description' not in st.session_state:
    st.session_state['description'] = ""
if 'food_name' not in st.session_state:
    st.session_state['food_name'] = ""
if 'calories' not in st.session_state:
    st.session_state['calories'] = 0
if 'proteins' not in st.session_state:
    st.session_state['proteins'] = 0.0
if 'carbs' not in st.session_state:
    st.session_state['carbs'] = 0.0
if 'fats' not in st.session_state:
    st.session_state['fats'] = 0.0
if 'generated_tags' not in st.session_state:
    st.session_state['generated_tags'] = []

# Page title
st.title("Menu Details Input")

# Food Name
st.session_state['food_name'] = st.text_input("Food Name", value=st.session_state['food_name'])

# Description
st.session_state['description'] = st.text_area("Description", height=100, value=st.session_state['description'])

# Button to generate description using Cohere
if st.button("Generate Description"):
    if st.session_state['food_name'] and st.session_state.current_ingredients:
        ingredients_list = ', '.join(st.session_state.current_ingredients)
        prompt = f"Write a detailed and appealing description for a dish called {st.session_state['food_name']} that includes ingredients like {ingredients_list}."
        try:
            response = co.generate(
                model='command-xlarge-nightly',
                prompt=prompt,
                max_tokens=80
            )
            generated_description = response.generations[0].text.strip()
            st.session_state['description'] = generated_description
            st.success("Description generated!")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter the food name and ingredients first.")

# Menu Photo
menu_photo = st.file_uploader("Upload Menu Photo", type=["jpg", "jpeg", "png"])

# Ingredients
st.subheader("Ingredients")
ingredient_input = st.text_input("Add Ingredient")
if st.button("Add Ingredient"):
    if ingredient_input:
        st.session_state.current_ingredients.append(ingredient_input)
        st.success(f"Ingredient added: {ingredient_input}")

st.write("Ingredients Added:")
for i, ingredient in enumerate(st.session_state.current_ingredients, 1):
    st.write(f"{i}. {ingredient}")

# Tags and Nutritional Value
st.subheader("Nutritional Value & Tags")
if st.button("Generate Nutritional Values & Tags"):
    if st.session_state['food_name'] and st.session_state.current_ingredients:
        ingredients_list = ', '.join(st.session_state.current_ingredients)
        prompt = f"""
        You are an AI specialized in predicting or estimating the number of calories and nutritional information of food items, and assigning appropriate dietary tags. 
        Analyze the following dish details and provide the calories, proteins, carbs, and fats, along with suitable dietary tags.
        Dish: {st.session_state['food_name']}
        Ingredients: {ingredients_list}
        Return the response in JSON format with keys 'calories', 'proteins', 'carbs', 'fats', and 'tags'.

        JSON Format: {{"calories": int, "proteins": float, "carbs": float, "fats": float, "tags": ["tag1", "tag2"]}}
        """

        try:
            response = co.generate(
                model='command-xlarge-nightly',
                prompt=prompt,
                max_tokens=100
            )
            generated_text = response.generations[0].text.strip()

            # Extract data using regular expressions or JSON parsing
            try:
                # If the response is valid JSON, load it directly
                data = json.loads(generated_text)
            except json.JSONDecodeError:
                # Fallback: extract with regex if JSON is malformed
                calories_match = re.search(r'"calories":\s*(\d+)', generated_text)
                proteins_match = re.search(r'"proteins":\s*(\d+\.?\d*)', generated_text)
                carbs_match = re.search(r'"carbs":\s*(\d+\.?\d*)', generated_text)
                fats_match = re.search(r'"fats":\s*(\d+\.?\d*)', generated_text)
                tags_match = re.search(r'"tags":\s*\[(.*?)\]', generated_text)

                data = {
                    'calories': int(calories_match.group(1)) if calories_match else 0,
                    'proteins': float(proteins_match.group(1)) if proteins_match else 0.0,
                    'carbs': float(carbs_match.group(1)) if carbs_match else 0.0,
                    'fats': float(fats_match.group(1)) if fats_match else 0.0,
                    'tags': [tag.strip().strip('"') for tag in tags_match.group(1).split(',')] if tags_match else []
                }

            st.session_state['calories'] = data.get('calories', 0)
            st.session_state['proteins'] = data.get('proteins', 0.0)
            st.session_state['carbs'] = data.get('carbs', 0.0)
            st.session_state['fats'] = data.get('fats', 0.0)
            st.session_state['generated_tags'] = data.get('tags', [])

            st.success("Nutritional values and tags generated!")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter the food name and ingredients first.")

# Display generated nutritional values and tags
st.write("**Generated Nutritional Values:**")
st.write(f"Calories: {st.session_state['calories']}")
st.write(f"Proteins: {st.session_state['proteins']}g")
st.write(f"Carbohydrates: {st.session_state['carbs']}g")
st.write(f"Fats: {st.session_state['fats']}g")

st.write("**Generated Tags:**")
st.write(', '.join(st.session_state['generated_tags']))

# Save Button
if st.button("Save"):
    # Store the details in session state
    st.session_state['menu_items'].append({
        'food_name': st.session_state['food_name'],
        'description': st.session_state['description'],
        'menu_photo': menu_photo,
        'ingredients': list(st.session_state.current_ingredients),  # Ensure this is a copy
        'tags': st.session_state['generated_tags'],
        'nutrition': {
            'calories': st.session_state['calories'],
            'proteins': st.session_state['proteins'],
            'carbs': st.session_state['carbs'],
            'fats': st.session_state['fats']
        }
    })
    st.success("Menu details saved successfully!")

    # Clear current ingredients for new entry
    st.session_state.current_ingredients.clear()
