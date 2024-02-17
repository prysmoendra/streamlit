# import library
import pandas as pd
import pickle
from PIL import Image
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px


# load template
px.defaults.template = 'plotly'
px.defaults.color_continuous_scale = 'reds'

# load image icon
# img = Image.open('../assets/dakota-dakode.jpeg')
# st.sidebar.image(img)

# buka file pickle
with open('data-input/used_data.pickle', 'rb') as f:
    data = pickle.load(f)

# SIDEBAR MENU
with st.sidebar:
    selected = option_menu(
         "Dakode Dashboard", ["Total Order", 
                              "Product Order"
        ], 
        icons = ['gear', 'gear'], 
        menu_icon = "house", 
        default_index = 0
        )
    
# dictionary for month
month_names = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}

# MENU TOTAL ORDER
if(selected == "Total Order"):
    st.title("Analysis Statistics Total Order")

    # set inputan tahun
    #============= data['year'] = data['year'].astype(str) =============
    years = ['All Years'] + list(data['year'].value_counts().keys().sort_values())
    year = st.selectbox(label='Range Year', options=years)

    # memfilter data tahun sesuai inputan yang diberikan
    outputs = data[(data['year'] == year)]

    # menampilkan visualisasi dengan bar chart
    st.header(':bar_chart: Order Total')

    if (year == 'All Years'):
        tab_year, tab_month, tab_day = st.tabs(['Year', 'Month', 'Day'])
        with tab_year:
            # st.header('for year')

            grouped_year_df = data.groupby('year')
            bar_data = grouped_year_df['order_item_id'].count()

            fig = px.bar(bar_data, color=bar_data, orientation='v', title=f"Most Orders of the Year  -  '{year}'")
            st.plotly_chart(fig)

            with st.expander("See explanation"):
                st.write(f" The chart above shows some numbers I picked for detail the most Order per Item. And this case the most Order per Item in 2018.")
        
        with tab_month:
            # st.header('for month')

            year_counts = data['year'].value_counts()
            most_freq_year = year_counts.idxmax()

            filtered_df = data[data['year'] == most_freq_year]
            grouped_month_df = filtered_df.groupby(['month'])
            outputs = grouped_month_df['order_item_id'].count()

            fig = px.bar(outputs, color=outputs, orientation='v', title=f"Most Orders of the Year  -  '{year}'")
            st.plotly_chart(fig)

            with st.expander("See explanation"):
                st.write(f" The chart above shows some numbers I picked for detail the most Order per Item in {most_freq_year}. And this case the most Order per Item in {most_freq_year} and in the month August, month number is 8.")
        
        with tab_day:
            # st.header('for day')

            month_counts = data['month'].value_counts()
            most_freq_month = month_counts.idxmax()

            df_day = filtered_df[filtered_df['month'] == most_freq_month]
            grouped_day_df = df_day.groupby(['day'])
            outputs = grouped_day_df['order_item_id'].count()

            fig = px.bar(outputs, color=outputs, orientation='v', title=f"Most Orders of the Year  -  '{year}' ,  the num. of Month  -  '{most_freq_month}  ({month_names[most_freq_month]})'")
            st.plotly_chart(fig)

            with st.expander("See explanation"):
                st.write(f" The chart above shows some numbers I picked for detail the most Order per Item in {most_freq_year}. And this case the most Order per Item in {most_freq_year} and in the month {month_names[most_freq_month]}. And at the Day 7 of month.")

    elif (year != 'All Years'):
        tab_year, tab_month, tab_day = st.tabs(['Year', 'Month', 'Day'])
        with tab_year:
            # st.header('for year')

            outputs = outputs[outputs['year'] == year]
            bar_data = outputs['order_item_id'].value_counts().nlargest(5)

            fig = px.bar(bar_data, color=bar_data, orientation='v', title=f"Most Orders of the Year  -  '{year}'")
            st.plotly_chart(fig)

            with st.expander("See explanation"):
                st.write(f" The chart above shows some numbers I picked for detail the most Order per Item. And this case the most Order per Item in {year}.")
            
        with tab_month:
            # st.header('for month')

            filtered_df = data[data['year'] == year]
            grouped_month_df = filtered_df.groupby(['month'])
            bar_data = grouped_month_df['order_item_id'].count()

            month_counts = filtered_df['month'].value_counts()
            most_freq_month = month_counts.idxmax()

            fig = px.bar(bar_data, color=bar_data, orientation='v', title=f"Most Orders of the Year  -  '{year}'")
            st.plotly_chart(fig)

            with st.expander("See explanation"):
                st.write(f" The chart above shows some numbers I picked for detail the most Order per Item in {year}. And this case the most Order per Item in {year} and in the month {month_names[most_freq_month]}, month number is {most_freq_month}.")
        
        with tab_day:
            # st.header('for day')

            month_counts = filtered_df['month'].value_counts()
            most_freq_month = month_counts.idxmax()

            df_day = filtered_df[filtered_df['month'] == most_freq_month]
            grouped_day_df = df_day.groupby(['day'])
            bar_data = grouped_day_df['order_item_id'].count()

            day_counts = df_day['day'].value_counts()
            most_freq_day = day_counts.idxmax()

            fig = px.bar(bar_data, color=bar_data, orientation='v', title=f"Most Orders of the Year  -  '{year}' ,  the num. of Month  -  '{most_freq_month}  ({month_names[most_freq_month]})'")
            st.plotly_chart(fig)

            with st.expander("See explanation"):
                st.write(f" The chart above shows some numbers I picked for detail the most Order per Item in {year}. And this case the most Order per Item in {year} and in the month {month_names[most_freq_month]}. And at the Day {most_freq_day} of month.")


# MENU PRODUCT ORDER
elif(selected == "Product Order"):
    st.title("Analysis Statistics per Product")

    # set inputan tanggal
    min_date = data['shipping_limit_date'].min()
    max_date = data['shipping_limit_date'].max()
    start_date, end_date = st.date_input(label='Range Date',
                                        min_value=min_date,
                                        max_value=max_date,
                                        value=[min_date, max_date])

    # set inputan product
    data['product'] = data['product'].astype(str)
    products = ['All Categories'] + list(data['product'].value_counts().keys().sort_values())
    product = st.selectbox(label='Category Product', options=products)

    # memfilter data sesuai inputan yang diberikan
    outputs = data[(data['shipping_limit_date'] >= start_date) &
                    (data['shipping_limit_date'] <= end_date)]
                    
    if (product != 'All Categories'):
        outputs = outputs[outputs['product'] == product]

    # menampilkan visualisasi dengan bar chart
    st.header(':chart_with_upwards_trend: Order Item')
    bar_data = outputs['order_item_id'].value_counts().nlargest(5)
    fig = px.bar(bar_data, color=bar_data, orientation='h', title=f"Pesanan terbanyak dari Category Product  '{product}'")
    st.plotly_chart(fig)
