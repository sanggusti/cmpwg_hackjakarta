import streamlit as st
import cohere
from dotenv import load_dotenv
import os
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
    st.session_state['tag_options'] = ["Vegan", "Vegetarian", "Gluten-Free", "Spicy", "Nut-Free"]
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
                max_tokens=100
            )
            generated_description = response.generations[0].text.strip()
            st.session_state['description'] = generated_description
            st.success("Description generated!")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please enter the food name and ingredients first.")

# Button to generate nutritional values using Cohere
if st.button("Generate Nutritional Values"):
    if st.session_state['food_name'] and st.session_state.current_ingredients:
        ingredients_list = ', '.join(st.session_state.current_ingredients)
        prompt = f"Estimate the nutritional values including calories, proteins, carbs, and fats for a dish called {st.session_state['food_name']} with ingredients like {ingredients_list}."
        try:
            response = co.generate(
                model='command-xlarge-nightly',
                prompt=prompt,
                max_tokens=100
            )
            generated_text = response.generations[0].text.strip()

            # Extract nutritional information from the generated text using regular expressions
            calories_match = re.search(r'calories:\s*(\d+)', generated_text, re.IGNORECASE)
            proteins_match = re.search(r'proteins:\s*(\d+\.?\d*)g', generated_text, re.IGNORECASE)
            carbs_match = re.search(r'carbs:\s*(\d+\.?\d*)g', generated_text, re.IGNORECASE)
            fats_match = re.search(r'fats:\s*(\d+\.?\d*)g', generated_text, re.IGNORECASE)

            st.session_state['calories'] = int(calories_match.group(1)) if calories_match else 0
            st.session_state['proteins'] = float(proteins_match.group(1)) if proteins_match else 0.0
            st.session_state['carbs'] = float(carbs_match.group(1)) if carbs_match else 0.0
            st.session_state['fats'] = float(fats_match.group(1)) if fats_match else 0.0

            st.success("Nutritional values generated!")
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

# Tags
st.subheader("Tags")
selected_tags = st.multiselect("Select Tags", options=st.session_state['tag_options'], default=[])

# Add New Tag
new_tag = st.text_input("Add a New Tag")
if st.button("Add Tag"):
    if new_tag and new_tag not in st.session_state['tag_options']:
        st.session_state['tag_options'].append(new_tag)
        st.success(f"Tag '{new_tag}' added!")
    elif new_tag:
        st.warning(f"Tag '{new_tag}' already exists.")

# Nutritional Value
st.subheader("Nutritional Value")
st.session_state['calories'] = st.number_input("Calories", min_value=0, step=1, value=st.session_state['calories'])
st.session_state['proteins'] = st.number_input("Proteins (g)", min_value=0.0, step=0.1, value=st.session_state['proteins'])
st.session_state['carbs'] = st.number_input("Carbohydrates (g)", min_value=0.0, step=0.1, value=st.session_state['carbs'])
st.session_state['fats'] = st.number_input("Fats (g)", min_value=0.0, step=0.1, value=st.session_state['fats'])

# Save Button
if st.button("Save"):
    # Store the details in session state
    st.session_state['menu_items'].append({
        'food_name': st.session_state['food_name'],
        'description': st.session_state['description'],
        'menu_photo': menu_photo,
        'ingredients': list(st.session_state.current_ingredients),  # Ensure this is a copy
        'tags': selected_tags,
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
