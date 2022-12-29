import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Sample Shop Dashboard",
                page_icon=":bar_char:",
                layout="wide"
                )

# clean data
# df = pd.read_csv('products.csv', encoding="ISO-8859-1")
# df.to_excel('productsCleaned.xlsx', index=None, header=True)

df = pd.read_excel(
    io='productsCleaned.xlsx'
)

# sidebar stuff
st.sidebar.header("Filters:")
category = st.sidebar.multiselect(
    "Select the Category:",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

df_selection = df.query(
    "Category == @category"
)

# Main
st.title(":bar_chart: Shop Dashboard :bar_chart:")
st.markdown("##")

# Top Stats
num_items = int(len(df_selection))
average_price = round(df_selection["Price"].mean(), 2)
num_categories = df_selection.Category.unique().size

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Number of Items:")
    st.subheader(f"{num_items}")
    
with middle_column:
    st.subheader("Average Price:")
    st.subheader(f"£ {average_price}")

with right_column:
    st.subheader("Number of Categories:")
    st.subheader(f"{num_categories}")

st.markdown("---")

# price by category
price_by_category = (
    df_selection.groupby(by=["Category"]).mean()[["Price"]].sort_values(by="Price")
)

fig_price_category = px.bar(
    price_by_category,
    x = "Price",
    y = price_by_category.index,
    orientation="h",
    title="<b>Average Prices by Category</b>",
    color_discrete_sequence=px.colors.sequential.RdBu,
)

# number of items per category as percentage
fig_percent_category = px.pie(
    df_selection, 
    names='Category',
    color_discrete_sequence=px.colors.sequential.RdBu,
    title="Categories by Percentage of Entire Shop"
)

# stylize
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_price_category, use_container_width = True)
right_column.plotly_chart(fig_percent_category, use_container_width = True)

# hide streamlit elems
hide_st_elems = """
<style>
#Main Menu {visiblity: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""

st.markdown(hide_st_elems, unsafe_allow_html=True)
