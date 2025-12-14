# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col # <-- functions (plural)

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie!")

# Name input
name_on_order = st.text_input("Name on Smoothie")
st.write("The name on your Smoothie will be:", name_on_order)

# Snowpark session
session = get_active_session()

# Get fruit options from Snowflake and prepare a Python list for Streamlit
my_dataframe = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"))
fruit_pd = my_dataframe.to_pandas()
fruit_options = fruit_pd["FRUIT_NAME"].dropna().astype(str).tolist()

# Multiselect (up to 5)
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    options=fruit_options
)

# Optional: enforce limit
if len(ingredients_list) > 5:
    st.error("Please select up to 5 ingredients.")
    st.stop()

# Build ingredients string (space-separated)
ingredients_string = " ".join(ingredients_list).strip()

# Escape single quotes to avoid breaking the SQL
safe_ingredients = ingredients_string.replace("'", "''")
safe_name = (name_on_order or "").replace("'", "''")

# Prepare INSERT (similar to original).
# Nota: ajusta las columnas según tu tabla real. Aquí asumo que existe 'ingredients' y 'name_on_order'.
my_insert_stmt = f"""
INSERT INTO smoothies.public.orders(ingredients, name_on_order)
VALUES ('{safe_ingredients}', '{safe_name}')
"""

# Submit button
time_to_insert = st.button("submit Order")

if time_to_insert:
    if not ingredients_list:
        st.warning("Please choose at least one ingredient before submitting.")
    else:
        session.sql(my_insert_stmt).collect()
        st.success("Your Smoothie is ordered!", icon="✅")
	
