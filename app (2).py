import streamlit as st

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go 
st.title("Tourism Insights in Lebanon 2023: Hotels, Restaurants, and Development Potential by Region")
st.write("This dataset provides an overview of Lebanon's tourism sector in 2023, highlighting development initiatives across various regions, offering insights into tourism potential and growth opportunities.")
path="https://linked.aub.edu.lb/pkgcube/data/f74a59420e9ef432f644575983b672b8_20240907_185056.csv"
df=pd.read_csv(path)
st.subheader("Fig1: 3D Plot of Tourism Index, Guest Houses, and Restaurants")
fig = px.scatter_3d(df, 
                    x='Tourism Index', 
                    y='Total number of guest houses', 
                    z='Total number of restaurants',
                    color='Tourism Index', 
                    title='3D Plot of Tourism Index, Guest Houses, and Restaurants',
                    labels={'Tourism Index': 'Tourism Index', 
                            'Total number of guest houses': 'Guest Houses', 
                            'Total number of restaurants': 'Restaurants'})
st.plotly_chart(fig)
st.subheader('Fig2: Tourism Index vs. Total Number of Restaurants')
fig_scatter = px.scatter(df, 
                        x='Tourism Index', 
                        y='Total number of restaurants', 
                        title='Tourism Index vs. Total Number of Restaurants', 
                        hover_data=['Town'])
st.plotly_chart(fig_scatter)
# Corrected Pie Chart
st.subheader('Fig3: Proportion of Towns with and without Hotels')
# Assuming you have columns 'Towns with Hotels' and 'Towns without Hotels'
# Preprocess data to create counts for the pie chart
hotel_data = df[['Town', 'Existence of hotels - does not exist']].copy()
hotel_data = hotel_data.groupby('Existence of hotels - does not exist').size().reset_index(name='Count')

fig_pie = px.pie(hotel_data, 
                 names='Existence of hotels - does not exist', 
                 values='Count', 
                 title='Proportion of Towns with and without Hotels')
st.plotly_chart(fig_pie)
st.subheader('Fig.4: Histogram of Tourism Index')
fig_hist = px.histogram(df, 
                        x='Tourism Index', 
                        title='Distribution of Tourism Index')
st.plotly_chart(fig_hist)
# Interactive features
st.sidebar.header('Interactive Features(I)')

# Slider to filter data based on Total Number of Guest Houses
guest_house_range = st.sidebar.slider('Select Range of Total Number of Guest Houses', 
                                      min_value=int(df['Total number of guest houses'].min()), 
                                      max_value=int(df['Total number of guest houses'].max()), 
                                      value=(int(df['Total number of guest houses'].min()), int(df['Total number of guest houses'].max())))

# Filter data based on the slider
filtered_df = df[(df['Total number of guest houses'] >= guest_house_range[0]) & 
                 (df['Total number of guest houses'] <= guest_house_range[1])]
st.sidebar.header('Interactive Features(II)')
# Slider to filter data based on Tourism Index
tourism_index_range = st.sidebar.slider('Select Tourism Index Range', 
                                        min_value=int(df['Tourism Index'].min()), 
                                        max_value=int(df['Tourism Index'].max()), 
                                        value=(int(df['Tourism Index'].min()), int(df['Tourism Index'].max())))
# Filter data based on the slider
filtered_df = df[(df['Tourism Index'] >= tourism_index_range[0]) & 
                 (df['Tourism Index'] <= tourism_index_range[1])]
# Dropdown to select plot type
plot_type = st.sidebar.selectbox('Select Plot Type', 
                                 options=['3D Scatter Plot', '2D Scatter Plot', 'Map View'])

# Display plots based on selected plot type
if plot_type == '3D Scatter Plot':
    st.subheader("Interactive Fig1: 3D Plot of Tourism Index, Guest Houses, and Restaurants")
    fig_3d = px.scatter_3d(filtered_df, 
                           x='Tourism Index', 
                           y='Total number of guest houses', 
                           z='Total number of restaurants',
                           color='Tourism Index', 
                           title='3D Plot of Tourism Index, Guest Houses, and Restaurants',
                           labels={'Tourism Index': 'Tourism Index', 
                                   'Total number of guest houses': 'Guest Houses', 
                                   'Total number of restaurants': 'Restaurants'})
    st.plotly_chart(fig_3d)

elif plot_type == '2D Scatter Plot':
    st.subheader('Interactive Fig2: Tourism Index vs. Total Number of Restaurants')
    fig_scatter = px.scatter(filtered_df, 
                            x='Tourism Index', 
                            y='Total number of restaurants', 
                            title='Tourism Index vs. Total Number of Restaurants', 
                            hover_data=['Town'])
    st.plotly_chart(fig_scatter)

elif plot_type == 'Map View':
    st.subheader('Interactive Map View of Tourism Data')
    if 'Latitude' in filtered_df.columns and 'Longitude' in filtered_df.columns:
        fig_map = px.scatter_mapbox(filtered_df, 
                                   lat='Latitude', 
                                   lon='Longitude', 
                                   color='Tourism Index', 
                                   size='Total number of guest houses', 
                                   hover_name='Town',
                                   mapbox_style='open-street-map', 
                                   title='Map View of Tourism Data')
        st.plotly_chart(fig_map)
    else:
        st.write("Map view requires 'Latitude' and 'Longitude' columns in the dataset.")
                                                              