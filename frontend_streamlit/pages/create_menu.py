import streamlit as st


st.set_page_config(
        page_title= "Create Menu",
        page_icon="🍛"
    )
# Initialize session state if it doesn't exist
if 'menu_items' not in st.session_state:
    st.session_state['menu_items'] = []
if 'current_ingredients' not in st.session_state:
    st.session_state['current_ingredients'] = []

# Page title
st.title("Menu Details Input")

# Food Name
food_name = st.text_input("Food Name")

# Description
description = st.text_area("Description", height=100)

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
tag_options = ["Vegan", "Vegetarian", "Gluten-Free", "Spicy", "Nut-Free"]
selected_tags = st.multiselect("Select Tags", options=tag_options, default=[])

# Add New Tag
new_tag = st.text_input("Add a New Tag")
if st.button("Add Tag"):
    if new_tag and new_tag not in tag_options:
        tag_options.append(new_tag)
        st.success(f"Tag '{new_tag}' added!")
    elif new_tag:
        st.warning(f"Tag '{new_tag}' already exists.")

# Nutritional Value
st.subheader("Nutritional Value")
calories = st.number_input("Calories", min_value=0, step=1)
proteins = st.number_input("Proteins (g)", min_value=0.0, step=0.1)
carbs = st.number_input("Carbohydrates (g)", min_value=0.0, step=0.1)
fats = st.number_input("Fats (g)", min_value=0.0, step=0.1)

# Save Button
if st.button("Save"):
    # Store the details in session state
    st.session_state['menu_items'].append({
        'food_name': food_name,
        'description': description,
        'menu_photo': menu_photo,
        'ingredients': st.session_state.current_ingredients,
        'tags': selected_tags,
        'nutrition': {
            'calories': calories,
            'proteins': proteins,
            'carbs': carbs,
            'fats': fats
        }
    })
    st.success("Menu details saved successfully!")

    st.session_state.current_ingredients = []

    # Clear the form
    food_name = ""
    description = ""
    
    selected_tags.clear()
    new_tag = ""
    calories = 0
    proteins = 0
    carbs = 0
    fats = 0

# Navigation
st.sidebar.header("Navigation")
if st.sidebar.button("Go to Collage"):
    st.rerun()
