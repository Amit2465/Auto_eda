import streamlit as st
import numpy as np
import pandas as pd



# Function to categorize columns and count data types
def categorize_data_types(df):
    categories = {
        'numeric': 0,
        'categorical': 0,
        'datetime': 0,
        'boolean': 0,
        'other': 0
    }

    column_categories = {}

    for col in df.columns:
        dtype = df[col].dtype

        if df[col].nunique() == 2:
            categories['boolean'] += 1
            column_categories[col] = 'boolean'
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            categories['datetime'] += 1
            column_categories[col] = 'datetime'
        elif pd.api.types.is_numeric_dtype(dtype):
            categories['numeric'] += 1
            column_categories[col] = 'numeric'    
        elif pd.api.types.is_object_dtype(dtype):
            try:
                parsed_dates = pd.to_datetime(df[col], errors='coerce')
                if parsed_dates.notna().all():
                    categories['datetime'] += 1
                    column_categories[col] = 'datetime'
                else:
                    categories['categorical'] += 1
                    column_categories[col] = 'categorical'
            except (TypeError, ValueError):
                categories['categorical'] += 1
                column_categories[col] = 'categorical'
        else:
            categories['other'] += 1
            column_categories[col] = 'other'

    return categories, column_categories
        
        


def check_warnings(df):
    warnings = []

    # High cardinality check
    for col in df.select_dtypes(include='object'):
        unique_count = df[col].nunique()
        total_count = len(df)
        if unique_count == total_count:
            warnings.append(f"<span style= 'background-color:#ffeeee; color:#aa3333; padding:4px; border-radius:4px; font-size:12px;'><i>{col}</i></span> has a high cardinality: {unique_count} distinct values")

    # Missing values check
    total_cells = np.prod(df.shape)
    missing_count = df.isnull().sum().sum()
    if missing_count > 0:
        missing_percentage = (missing_count / total_cells) * 100
        for col in df.columns:
            col_missing = df[col].isnull().sum()
            if col_missing > 0:
                col_missing_percentage = (col_missing / total_count) * 100
                warnings.append(f"<span style='background-color:#ffeeee; color:#aa3333; padding:4px; border-radius:4px; font-size:12px;'><i>{col}</i></span> has {col_missing} ({col_missing_percentage:.1f}%) missing values")

    # Zeros check for numerical columns
    for col in df.select_dtypes(include=['int64', 'float64']):
        zero_count = (df[col] == 0).sum()
        total_count = len(df)
        if zero_count > 0:
            zero_percentage = (zero_count / total_count) * 100
            warnings.append(f"<span style='background-color:#ffeeee; color:#aa3333; padding:4px; border-radius:4px; font-size:12px;'><i>{col}</i></span> has {zero_count} ({zero_percentage:.1f}%) zeros")

    # Duplicates check
    duplicate_count = df.duplicated().sum()
    if duplicate_count > 0:
        duplicate_percentage = (duplicate_count / total_count) * 100
        warnings.append(f"<span style='background-color:#ffeeee; color:#aa3333; padding:4px; border-radius:4px; font-size:12px;'>There are {duplicate_count} ({duplicate_percentage:.1f}%) duplicate rows</span>")

    # Correlations check (only for numerical columns)
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    if len(numeric_cols) > 1:   
        corr_matrix = df[numeric_cols].corr().abs()
        upper_tri = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
        correlated_pairs = [(col1, col2) for col1 in upper_tri.columns for col2 in upper_tri.columns if upper_tri[col1][col2] > 0.8]
        for pair in correlated_pairs:
            warnings.append(f"<span style='background-color:#ffeeee; color:#aa3333; padding:4px; border-radius:4px; font-size:12px;'><i>{pair[0]}</i> and <i>{pair[1]}</i></span> is highly correlated")

    return warnings





def generate_warning_badge(warning_type):
    badge_colors = {
        'High cardinality': '#FF8C6A',   
        'Missing values': '#FFA500',     
        'Zeros': '#808080',              
        'Duplicates': '#0066CC',         
        'Correlations': '#5CB85C'        
    }

    badge_color = badge_colors.get(warning_type, '#FFFFFF')  
    badge_text = warning_type if warning_type else 'Unknown'

    badge_html = f'<span style="background-color:{badge_color}; color:white; padding:5px; border-radius:5px; display:inline-block; min-width:80px; text-align:center; font-size:10px;">{badge_text}</span>'
    return badge_html


def overview_main(df):
    st.markdown("## Overview")    
    st.markdown('</br>', unsafe_allow_html=True)
    tab1, tab2 = st.tabs([':notebook: Overview', ':warning: Warnings'])
    with tab1:
        col1, col2, = st.columns((2))
        with col1:
            st.markdown('#### Dataset statistics')
            st.markdown('</br>', unsafe_allow_html=True)
            col3,col4 = st.columns((2))
            with col3:
                st.markdown('Number of variables')
                st.markdown('Number of observations')
                st.markdown('Missing cells')
                st.markdown('Missing cells (%)')
                st.markdown('Duplicate rows')
                st.markdown('Duplicate rows (%)')
                st.markdown('Total size in memory')
                st.markdown('Average record size in memory')
            with col4:
                st.markdown(f"<span style='color: green; font-style: italic;'>{len(df.columns)}", unsafe_allow_html=True)
                st.markdown(f"<span style='color: green; font-style: italic;'>{len(df)}", unsafe_allow_html=True)
                st.markdown(f"<span style='color: green; font-style: italic;'>{df.isnull().sum().sum()}", unsafe_allow_html=True)
                st.markdown(f"<span style='color: green; font-style: italic;'>{(df.isnull().sum().sum() / df.size) * 100:.1f}%", unsafe_allow_html=True)
                st.markdown(f"<span style='color: green; font-style: italic;'>{df.duplicated().sum()}", unsafe_allow_html=True)
                st.markdown(f"<span style='color: green; font-style: italic;'>{(df.duplicated().sum() / len(df)) * 100:.1f}%", unsafe_allow_html=True)
                st.markdown(f"<span style='color: green; font-style: italic;'>{df.memory_usage().sum() / 1024:.1f} KiB", unsafe_allow_html=True)
                st.markdown(f"<span style='color: green; font-style: italic;'>{df.memory_usage(index=True).mean():.1f} B", unsafe_allow_html=True)
        
        with col2:
            st.markdown('#### Variable types')
            st.markdown('</br>', unsafe_allow_html=True)
            col5,col6 = st.columns((2))
            with col5:
                for category, count in categorize_data_types(df)[0].items():
                    if count > 0:
                        st.markdown(f"{category.capitalize()}", unsafe_allow_html=True)
                            
            with col6:
                for category, count in categorize_data_types(df)[0].items():
                    if count > 0:
                        st.markdown(f"<span style='color: green; font-style: italic;'>{count}", unsafe_allow_html=True)
    
    
    with tab2:
        col1, col2 = st.columns((2))
        with col1:
            warnings = check_warnings(df)
            if len(warnings) == 0:
                st.info("No warnings found.")
            else:
                for warning in warnings:
                    st.markdown(warning, unsafe_allow_html=True)
                    
        with col2:
            for warning in warnings:
                if "high cardinality" in warning:
                    st.markdown(generate_warning_badge('High cardinality'), unsafe_allow_html=True)
                elif "missing values" in warning:
                    st.markdown(generate_warning_badge('Missing values'), unsafe_allow_html=True)
                elif "zeros" in warning:
                    st.markdown(generate_warning_badge('Zeros'), unsafe_allow_html=True)
                elif "duplicate" in warning:
                    st.markdown(generate_warning_badge('Duplicates'), unsafe_allow_html=True)
                elif "correlated" in warning:
                    st.markdown(generate_warning_badge('Correlations'), unsafe_allow_html=True)
         
    