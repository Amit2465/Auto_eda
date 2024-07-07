import streamlit as st
import matplotlib.pyplot as plt
import missingno as msno
from Sample import custom_css_box

# Function to visualize missing values in the dataset
def missing_values(df):
    st.markdown('### Missing Values')      
    tab1, tab2, tab3, tab4 = st.tabs([":pencil: Count", "𝄜 Matrix", " :fire: Heatmap", " 🌳 dendrogram"])
     
    
    with tab1:
        # Count of missing values in each column displayed as a bar chart
        st.markdown('### Count')
        col1, col2 = st.columns((2))
        with col2:
            st.markdown('</br>', unsafe_allow_html= True)
            st.markdown('</br>', unsafe_allow_html= True)
            st.markdown('</br>', unsafe_allow_html= True)
            sample_text = """
                            The Count summarizes missing values in each column of the dataset.
                            It displays the number of missing values for each attribute, aiding in understanding
                            data completeness and identifying columns that may require imputation or further
                            investigation.
                            """            
            custom_css_box(sample_text)
            
        with col1:
            fig, ax = plt.subplots(figsize=(4, 2))
            msno.bar(df, ax=ax, fontsize=8)
            ax.tick_params(axis='x', labelsize=8)
            st.pyplot(fig)
            plt.clf()
            plt.close(fig)
    
    with tab2:
        # Matrix view of missing data patterns across the dataset
        st.markdown('### Matrix')
        col4, col3 = st.columns((2))
        with col3: 
            st.markdown('</br>', unsafe_allow_html= True)
            st.markdown('</br>', unsafe_allow_html= True)
            st.markdown('</br>', unsafe_allow_html= True)
            text2 =  '''The Matrix visualizes missing data patterns across the entire dataset using a 
                        matrix-like display. It provides a comprehensive overview of missing values, 
                        highlighting their presence with blank or color-coded cells. This visualization helps 
                        detect correlations in missingness between different columns, guiding decisions on data 
                        preprocessing and analysis strategies.'''
            custom_css_box(text2)            
            
        with col4:
            fig, ax = plt.subplots(figsize=(4, 2))
            msno.matrix(df, ax=ax, fontsize=8)
            ax.tick_params(axis='x', labelsize=8)
            st.pyplot(fig)
            plt.clf()
            plt.close(fig)
        
    with tab3:
        # Heatmap visualization of missing data patterns
        st.markdown('### Heatmap')
        col6,col5 = st.columns((2))
        with col5:
            st.markdown('</br>', unsafe_allow_html= True)
            text3 =  '''The Heatmap visually represents missing data patterns across the dataset.
                        It helps in understanding the distribution of missing values, highlighting variables 
                        with missing data and their locations.'''
            custom_css_box(text3)
                        
        with col6:
            fig, ax = plt.subplots(figsize=(4, 2))
            msno.heatmap(df, ax=ax, fontsize=8)
            ax.tick_params(axis='x', labelsize=8)
            st.pyplot(fig)
            plt.clf()
            plt.close(fig)
    
    with tab4:
        # Dendrogram visualization of hierarchical clustering based on missing data
        st.markdown('### Dendrogram')
        col8,col7 = st.columns((2))
        
        with col7:
            st.markdown('</br>', unsafe_allow_html= True)
            text4 = '''The Dendrogram displays hierarchical clustering of variables based on their
                        missing data patterns. It helps understand relationships among variables with 
                        similar missingness profiles, highlighting clusters that may share common missing 
                        data characteristics.'''
            custom_css_box(text4)            
            
        with col8:
            fig, ax = plt.subplots(figsize=(8, 2))
            msno.dendrogram(df, ax=ax, fontsize=8)
            ax.tick_params(axis='x', labelsize=8)
            st.pyplot(fig)
            plt.clf()
            plt.close(fig)