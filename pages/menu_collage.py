import streamlit as st

# Function to define the layout size based on the index
def get_layout_size(index):
    if index % 3 == 0:
        return 3
    elif index % 3 == 1:
        return 1
    else:
        return 2

# Page title
st.title("Menu Collage")

# Check if there are any saved menu items
if 'menu_items' in st.session_state and st.session_state['menu_items']:
    items = st.session_state['menu_items']

    for index, item in enumerate(items):
        # Determine column layout size
        col_size = get_layout_size(index)
        cols = st.columns(col_size)
        
        with cols[0]:  # Using the first column for displaying content
            # Display menu photo if available
            if item['menu_photo'] is not None:
                st.image(item['menu_photo'], caption=item['food_name'], use_column_width=True)
            else:
                st.write(item['food_name'])
            
            st.write(item['description'])
            st.write("Ingredients: ", ", ".join(item['ingredients']))
            st.write("Tags: ", ", ".join(item['tags']))
            with st.expander("Nutritional Value"):
                st.write(f"Calories: {item['nutrition']['calories']} kcal")
                st.write(f"Proteins: {item['nutrition']['proteins']} g")
                st.write(f"Carbohydrates: {item['nutrition']['carbs']} g")
                st.write(f"Fats: {item['nutrition']['fats']} g")
else:
    st.write("No menu items to display.")

# Navigation
st.sidebar.header("Navigation")
if st.sidebar.button("Go to Input Form"):
    st.rerun()
