# Import python packages.
import streamlit as st
from snowflake.snowpark.functions import (col)
import requests  

st.set_page_config(layout="wide")

# Write directly to the app.
st.title(f":cup_with_straw: Customize Your Smoothie!:cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

name_on_order = st.text_input('Name on Smoothie:')
if name_on_order:
    st.write('The name on your Smoothie will be: ', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
df = session.table('smoothies.public.fruit_options').select(col("FRUIT_NAME"))
#st.dataframe(data=df, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    , df
    ,placeholder='Select from list'
    #,max_selections=5
)

if ingredients_list:
    
    if len(ingredients_list) > 5:
        st.warning("Please select no more than 5 ingredients.")
        #ingredients_list = ingredients_list[:5]
    else:
        ingredients_string = ''
        for fruit_chosen in ingredients_list:
            ingredients_string += fruit_chosen + ' '
    
            my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
                        values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
    
        
        time_to_insert = st.button('Submit Order')
    
        if time_to_insert:
            session.sql(my_insert_stmt).collect()
            
            st.success('Your Smoothie is ordered, '+name_on_order+'!', icon="✅")

smoothiefroot_response = requests.get("[https://my.smoothiefroot.com/api/fruit/watermelon](https://my.smoothiefroot.com/api/fruit/watermelon)")  
st.text(smoothiefroot_response)
