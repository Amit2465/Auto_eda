import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from Variables import categorize_column_type


def select_columns_by_type(df):
    selected_columns = []
    
    for col in df.columns:
        if df[col].dtype == 'object' or pd.api.types.is_categorical_dtype(df[col]):
            unique_count = df[col].nunique()
            if unique_count < 12 and unique_count >= 2:
                selected_columns.append(col)
        else:
            selected_columns.append(col)
    
    return selected_columns




def plot_numeric_vs_numeric(df, x, y):
    col1, col2 = st.columns((2))
    with col1:  
        scatter_fig = px.scatter(df, x=x, y=y, title=f'Scatter Plot: {x} vs {y}', labels={x: x, y: y})
        st.plotly_chart(scatter_fig)
        
    with col2:
        hist_fig = px.histogram(df, x=x, y=y, title=f'Histogram: {x} vs {y}', labels={x: x, y: y})
        st.plotly_chart(hist_fig)
    
    col3, col4 = st.columns((2))
    with col3:
        density_fig = px.density_contour(df, x=x, y=y, marginal_x="histogram", marginal_y="histogram", title=f'Density Plot: {x} vs {y}', labels={x: x, y: y})
        st.plotly_chart(density_fig)
        
    with col4:
        area_fig = px.area(df, x=x, y=y, title=f'Area Chart: {x} vs {y}', labels={x: x, y: y})
        st.plotly_chart(area_fig)
    
    col5 , col6 = st.columns((2))
    with col5:
        joint_fig = px.scatter(df, x=x, y=y, marginal_x="histogram", marginal_y="histogram", title=f'Joint Plot: {x} vs {y}', labels={x: x, y: y})
        st.plotly_chart(joint_fig)
    
    with col6:
        pass
 
 
def plot_numeric_vs_categorical(df, x, y):
    col1, col2 = st.columns((2, 2))

    with col1:
        box_fig = px.box(df, x=y, y=x, title=f'Box Plot: {y} by {x}', points='all')
        st.plotly_chart(box_fig)
        
    with col2:
        bar_fig = px.bar(df, x=y, y=x, color=y, title=f'Bar Plot: {y} by {x}', labels={x: x, y: y})
        st.plotly_chart(bar_fig)

    col3, col4 = st.columns((2))
    with col3:
        violin_fig = px.violin(df, x=y, y=x, title=f'Violin Plot: {y} by {x}', box=True, points='all')
        st.plotly_chart(violin_fig)
        
    with col4:        
        strip_fig = px.strip(df, x=y, y=x, title=f'Strip Plot: {y} by {x}', color=y)
        st.plotly_chart(strip_fig)


    col5, col6 = st.columns((2))

    with col5:
        bar_chart_fig = px.bar(df, x=x, y=y, title=f'Bar Chart: {y} by {x}', color=y)
        st.plotly_chart(bar_chart_fig)

    with col6:
        pass


def plot_numeric_vs_boolean(df, x, y):
    col1, col2 = st.columns((2))
    with col1:
        scatter_fig = px.scatter(df, x=x, y=y, title=f'Scatter Plot: {x} vs {y}', labels={x: x, y: y})
        st.plotly_chart(scatter_fig)
    with col2:
        bar_fig = px.bar(df, x=y, y=x, color=y, title=f'Bar Plot: {y} by {x}', labels={x: x, y: y})
        st.plotly_chart(bar_fig)
    
    col3, col4 = st.columns((2))
    with col3:
        hist_fig = px.histogram(df, x=x, y=y, title=f'Histogram: {x} vs {y}', labels={x: x, y: y})
        st.plotly_chart(hist_fig)
    
    with col4:
        box_fig = px.box(df, x=y, y=x, title=f'Box Plot: {y} by {x}', points='all')
        st.plotly_chart(box_fig)
 


def plot_numeric_vs_datetime(df, x, y):
    col1 , col2 = st.columns((2))
    with col1:
        line_fig = px.line(df, x=x, y=y, title=f'Line Plot: {x} vs {y}', labels={x: x, y: y})
        st.plotly_chart(line_fig)
    with col2:
        scatter_fig = px.scatter(df, x=x, y=y, title=f'Scatter Plot: {x} vs {y}', labels={x: x, y: y})
        st.plotly_chart(scatter_fig) 
    
    col3, col4 = st.columns((2))
    with col3:
        bar_chart_fig = px.bar(df, x=x, y=y, title=f'Bar Chart: {y} by {x}', color=y)
        st.plotly_chart(bar_chart_fig)  
            
    with col4:
        hist_fig = px.histogram(df, x=x, y=y, title=f'Histogram: {x} vs {y}', labels={x: x, y: y})
        st.plotly_chart(hist_fig)
    
    col5, col6 = st.columns((2))
    with col5:
        area_fig = px.area(df, x=x, y=y, title=f'Area Chart: {x} vs {y}', labels={x: x, y: y})
        st.plotly_chart(area_fig)
    with col6:
        box_fig = px.box(df, x=y, y=x, title=f'Box Plot: {y} by {x}', points='all')
        st.plotly_chart(box_fig)                                                                 
    
    col7, col8 = st.columns((2))
    with col7:
        density_fig = px.density_contour(df, x=x, y=y, marginal_x="histogram", marginal_y="histogram", title=f'Density Plot: {x} vs {y}', labels={x: x, y: y})
        st.plotly_chart(density_fig)
    with col8:
        violin_fig = px.violin(df, x=y, y=x, title=f'Violin Plot: {y} by {x}', box=True, points='all')
        st.plotly_chart(violin_fig)



def plot_categorical_vs_categorical(df, x, y):
    col1, col2 = st.columns((2))
    with col1:
        bar_fig = px.bar(df, x=x, y=y, color=x, title=f'Bar Plot: {y} by {x}', labels={x: x, y: y})
        st.plotly_chart(bar_fig)
    with col2:
        fig_pie = px.pie(df, names=x, title=f'Pie Chart: {y}')
        st.plotly_chart(fig_pie)
    
    col3, col4 = st.columns((2))
    with col3:
        fig_stack = px.bar(df, x=x, color=y, title=f'Stacked Bar Chart: {x} vs {y}', barmode='stack')
        st.plotly_chart(fig_stack)
    with col4:
        fig_heatmap = px.density_heatmap(df, x=x, y=y, title=f'Heatmap: {x} vs {y}')
        st.plotly_chart(fig_heatmap)
    
    col5, col6 = st.columns((2))
    with col5:
        fig_sunburst = px.sunburst(df, path=[x, y], title=f'Sunburst Plot: {x} vs {y}')
        st.plotly_chart(fig_sunburst)
    with col6:
        fig_cluster = px.bar(df, x=x, color=y, title=f'Clustered Bar Chart: {x} vs {y}', barmode='group')
        st.plotly_chart(fig_cluster)       
    
                

def plot_categorical_vs_boolean(df, x, y):
    col1 , col2 = st.columns((2))
    with col1:
        bar_fig = px.bar(df, x=x, y=y, color=x, title=f'Bar Plot: {y} by {x}', labels={x: x, y: y})
        st.plotly_chart(bar_fig)
    with col2:
        pass
    
    

def plot_boolean_vs_boolean(df,x,y):
    co1, co2 = st.columns(2)
    
    with co1:
        fig_cluster = px.bar(df, x=x, color=y, title=f'Clustered Bar Chart: {x} vs {y}', barmode='group')
        st.plotly_chart(fig_cluster)
    with co2:
        pass
        
    
    

def interaction(df):
    st.markdown('## Interaction')
    st.markdown('---')

    columns = select_columns_by_type(df)
    x = st.selectbox('Select first column', columns)
    y = st.selectbox('Select second column', columns)

    st.markdown('</br>', unsafe_allow_html=True)

    col1_type = categorize_column_type(df, x)
    col2_type = categorize_column_type(df, y)

    if col1_type == 'numeric' and col2_type == 'numeric':
        plot_numeric_vs_numeric(df, x, y)
    elif col1_type == 'numeric' and col2_type == 'categorical':
        plot_numeric_vs_categorical(df, x, y)
    elif col1_type == 'categorical' and col2_type == 'numeric':
        plot_numeric_vs_categorical(df, x,y)
    elif col1_type == 'numeric' and col2_type == 'boolean':
        plot_numeric_vs_boolean(df,x,y)
    elif col1_type == 'boolean' and col2_type == 'numeric':            
        plot_numeric_vs_boolean(df,x,y)
    elif col1_type == 'numeric' and col2_type == 'datetime':            
        plot_numeric_vs_datetime(df,x,y)
    elif col1_type == 'datetime' and col2_type == 'numeric':            
        plot_numeric_vs_datetime(df,x,y)
    elif col1_type == 'categorical' and col2_type == 'categorical':
        plot_categorical_vs_categorical(df,x,y)
    elif col1_type == 'categorical' and col2_type == 'boolean':
        plot_categorical_vs_boolean(df,x,y)
    elif col1_type == 'boolean' and col2_type == 'categorical':
        plot_categorical_vs_boolean(df,x,y)
    elif col1_type == 'boolean' and col2_type == 'boolean':
        plot_categorical_vs_boolean(df,x,y)
                            
    else: 
        st.write(f'Plots for column type {col1_type} and {col2_type} are not implemented yet.')

            