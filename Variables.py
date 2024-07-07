import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from scipy.stats import kurtosis, skew
import statistics
from astropy.stats import bayesian_blocks



def calculate_mad(df, column):
    mean = statistics.mean(df[column])
    abs_deviation = [abs(x - mean) for x in df[column]]
    mad = statistics.mean(abs_deviation)
    
    return mad



def click_button():
    st.session_state.button = not st.session_state.button
    
    

def categorize_column_type(df, column):
    dtype = df[column].dtype

    if df[column].nunique() == 2:
            return 'boolean'            
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return 'datetime'        
    elif pd.api.types.is_numeric_dtype(dtype):
        return 'numeric'            
    elif pd.api.types.is_object_dtype(dtype):
        try:
            parsed_dates = pd.to_datetime(df[column], errors='coerce')
            if parsed_dates.notna().all():
                return 'datetime'                
            else:
                return 'categorical'                
        except (TypeError, ValueError):
            return 'categorical'
    else:
        return 'other'


def column_characteristics(df, col):
    characteristics = []
    
    if df[col].nunique() == 1:
        characteristics.append('UNIFORM')
   
    if df[col].nunique() == len(df[col]):
        characteristics.append('UNIQUE')

    if df[col].nunique() > len(df[col]) / 2:
        characteristics.append('HIGH CARDINALITY')
   
    if df[col].isnull().any():
        characteristics.append('MISSING')

    if (df[col] == 0).sum() > 0:
        characteristics.append('ZEROS')

    return characteristics


def generate_badge(df, column):
    for ch in column_characteristics(df, column):
        st.markdown(f"<span style='background-color:#ffeeee; color:#aa3333; padding:4px; border-radius:4px; font-size:12px;'>{ch}</span>", unsafe_allow_html= True)  


def value_count(df, column, top_n=10):
    try:
        value_counts = df[column].value_counts()
        top_values_dict = {}
        
        if len(value_counts) <= top_n:
            for value, count in value_counts.items():
                top_values_dict[value] = count
        else:
            for value, count in value_counts.head(top_n).items():
                top_values_dict[value] = count
            if len(value_counts) > top_n:
                other_count = value_counts.iloc[top_n:].sum()  
                top_values_dict['Other'] = other_count
    except Exception as e:
        st.warning(f"Error calculating value counts for column '{column}': {e}")
        top_values_dict = {}
    
    return top_values_dict


def calculate_frequency_percent(value, count, df, column):    
    total_count = df[column].sum()
    percentage = (count / total_count) * 100
    return percentage

def find_min_values(df, column, n=5):
    value_counts = df[column].value_counts()
    sorted_values = value_counts.sort_index()
    min_values = sorted_values.head(n).to_dict()
    return min_values

def find_max_values(df, column, n=5):
    value_counts = df[column].value_counts()
    sorted_values = value_counts.sort_index(ascending=False)
    max_values = sorted_values.head(n).to_dict()
    return max_values


def calculate_length_metrics(df,column):
    max_length = df[column].str.len().max()
    mean_length = df[column].str.len().mean()
    min_length = df[column].str.len().min()
    return max_length, mean_length, min_length


def character_count_from_df(df, column):
    lowercase_count = 0
    uppercase_count = 0
    other_punctuation_count = 0
    close_punctuation_count = 0
    space_separator_count = 0
    open_punctuation_count = 0
    dash_punctuation_count = 0
    
    for string in df[column]:
        if pd.notna(string):  # Check if string is not NaN
            for char in string:
                if char.islower():
                    lowercase_count += 1
                elif char.isupper():
                    uppercase_count += 1
                elif char in '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~':
                    other_punctuation_count += 1
                    if char in ')]:':
                        close_punctuation_count += 1
                    elif char in '([{':
                        open_punctuation_count += 1
                    elif char == '-':
                        dash_punctuation_count += 1
                elif char.isspace():
                    space_separator_count += 1
    
    # Store counts in a dictionary
    counts_dict = {
        'Lowercase_Letter': lowercase_count,
        'Uppercase_Letter': uppercase_count,
        'Other_Punctuation': other_punctuation_count,
        'Close_Punctuation': close_punctuation_count,
        'Space_Separator': space_separator_count,
        'Open_Punctuation': open_punctuation_count,
        'Dash_Punctuation': dash_punctuation_count
    }
    
    return counts_dict




def numerical_column(df,column):
    col1, col2, col3, col4 = st.columns((4))
    with col1:
        column_type = categorize_column_type(df, column)
        cc = column_characteristics(df,column)
        st.markdown(f"{column_type}")
        generate_badge(df,column)        
    with col2:
        col1 , col2 = st.columns((2))
        with col1:
            if "UNIQUE" in cc:
                st.markdown('<span style="color:#aa3333;">Distinct count</span>', unsafe_allow_html=True)
                st.markdown('<span style="color:#aa3333;">Unique(%)</span>', unsafe_allow_html=True)
            else:
                st.markdown("Distinct count")
                st.markdown("Unique(%)")
            if 'MISSING' in cc:        
                st.markdown('<span style="color:#aa3333;">Missing</span>', unsafe_allow_html=True)
                st.markdown('<span style="color:#aa3333;">Missing(%)</span>', unsafe_allow_html=True)
            else:
                st.markdown("Missing")
                st.markdown("Missing (%)")    
            st.markdown("Infinite")
            st.markdown("Infinite (%)")
        with col2:
            st.markdown(f"<span style='color: green; font-style: italic;'>{round(df[column].nunique(), 3)}", unsafe_allow_html=True)
            st.markdown(f"<span style='color: green; font-style: italic;'>{round((df[column].nunique() / len(df[column])) * 100 , 3) if len(df[column]) > 0 else 0}", unsafe_allow_html=True)
            st.markdown(f"<span style='color: green; font-style: italic;'>{round(df[column].isnull().sum(), 3)}", unsafe_allow_html=True)
            st.markdown(f"<span style='color: green; font-style: italic;'>{round((df[column].isnull().sum() / len(df[column])) * 100, 3) if len(df[column]) > 0 else 0}", unsafe_allow_html=True)
            st.markdown(f"<span style='color: green; font-style: italic;'>{round(np.isinf(df[column].astype(float)).sum(), 3)}</span>", unsafe_allow_html=True)
            st.markdown(f"<span style='color: green; font-style: italic;'>{round((np.isinf(df[column].astype(float)).sum() / len(df[column]) * 100 if len(df[column]) > 0 else 0 ), 3):.2f}%</span>", unsafe_allow_html=True)
 
    with col3:
        col1 , col2 = st.columns((2))
        with col1:
            st.markdown("Mean")
            st.markdown("Minimum")
            st.markdown("Maximum")
            if "ZEROS" in cc:
                st.markdown('<span style="color:#aa3333;">Zeros</span>', unsafe_allow_html=True)
                st.markdown('<span style="color:#aa3333;">Zeros (%)</span>', unsafe_allow_html=True)
            else:
                st.markdown("Zeros")
                st.markdown("Zeros (%)")    
            st.markdown("Memory size")
        with col2:
                st.markdown(f"<span style='color: green; font-style: italic;'>{round(df[column].mean() , 3)}", unsafe_allow_html=True)
                st.markdown(f"<span style='color: green; font-style: italic;'>{round(df[column].min(), 3)}", unsafe_allow_html=True)
                st.markdown(f"<span style='color: green; font-style: italic;'>{round(df[column].max(), 3)}", unsafe_allow_html=True)
                st.markdown(f"<span style='color: green; font-style: italic;'>{round((df[column]==0).sum(), 3)}", unsafe_allow_html=True)
                st.markdown(f"<span style='color: green; font-style: italic;'>{round(((df[column]==0).sum() / len(df[column])) * 100 ,3)if len(df[column]) > 0 else 0}", unsafe_allow_html=True)
                st.markdown(f"<span style='color: green; font-style: italic;'>{round(df[column].memory_usage(deep=True) / 1024, 3)} KiB</span>", unsafe_allow_html=True)

       
    with col4:
        pass


def toggle_button_for_numeric(df, column):
    unique_key = f"button_{column}"
    if 'button' not in st.session_state:
        st.session_state.button = False     

    st.button('Toggle details', key=unique_key, on_click=click_button)

    if st.session_state.button:
        tab1, tab2, tab3, tab4 = st.tabs(['Statistics', 'Histogram(s)', 'Common values', 'Extrem values'])
        with tab1:
            col1, col2 = st.columns((2))
            with col1:
                col7 , col8 = st.columns((2))
                with col7:
                    st.markdown("<b> Quantile statistics </b>", unsafe_allow_html= True)
                    st.markdown("</br>", unsafe_allow_html=True)
                    st.markdown("<div>Minimum</div>", unsafe_allow_html=True)
                    st.markdown("<div>5-th percentile</div>", unsafe_allow_html=True)
                    st.markdown("<div>Q1</div>", unsafe_allow_html=True)
                    st.markdown("<div>median</div>", unsafe_allow_html=True)
                    st.markdown("<div>Q3</div>", unsafe_allow_html=True)
                    st.markdown("<div>95-th percentile</div>", unsafe_allow_html=True)
                    st.markdown("<div>Maximum</div>", unsafe_allow_html=True)
                    st.markdown("<div>Range</div>", unsafe_allow_html=True)
                    st.markdown("<div>Interquartile range (IQR)</div>", unsafe_allow_html=True)
                with col8:
                    st.markdown("</br>", unsafe_allow_html=True)
                    st.markdown("</br>", unsafe_allow_html=True)
                    st.markdown("</br>", unsafe_allow_html=True)
                    st.markdown("</br>", unsafe_allow_html=True)
                    st.markdown(f"<div style='color: green; font-style: italic;'</div>{round(df[column].min(), 3)}", unsafe_allow_html=True)
                    st.markdown(f"<div style='color: green; font-style: italic;'</div>{round(df[column].quantile(0.05), 3)}", unsafe_allow_html=True)
                    st.markdown(f"<div style='color: green; font-style: italic;'</div>{round(df[column].quantile(0.25), 3)}", unsafe_allow_html=True)
                    st.markdown(f"<div style='color: green; font-style: italic;'</div>{round(df[column].median(), 3)}", unsafe_allow_html=True)
                    st.markdown(f"<div style='color: green; font-style: italic;'</div>{round(df[column].quantile(0.75), 3)}", unsafe_allow_html=True)
                    st.markdown(f"<div style='color: green; font-style: italic;'</div>{round(df[column].quantile(0.95), 3)}", unsafe_allow_html=True)
                    st.markdown(f"<div style='color: green; font-style: italic;'</div>{round(df[column].max(), 3)}", unsafe_allow_html=True)
                    st.markdown(f"<div style='color: green; font-style: italic;'</div>{round(df[column].max() - df[column].min(), 3)}", unsafe_allow_html=True)
                    st.markdown(f"<div style='color: green; font-style: italic;'</div>{round(df[column].quantile(0.75) - df[column].quantile(0.25), 3)}", unsafe_allow_html=True)
                    
                        
            with col2:
                col9 , col10 = st.columns((2))
                with col9:
                    st.markdown("<b> Descriptive statistics </b>", unsafe_allow_html=True)
                    st.markdown("</br>", unsafe_allow_html= True)
                    st.markdown("<div> Standard deviation </div>", unsafe_allow_html=True)
                    st.markdown("<div> Coefficient of variation (CV) </div>", unsafe_allow_html=True)
                    st.markdown("<div> Kurtosis </div>", unsafe_allow_html=True)
                    st.markdown("<div> Mean </div>", unsafe_allow_html=True)
                    st.markdown("<div> Median Absolute Deviation (MAD) </div>", unsafe_allow_html=True)
                    st.markdown("<div> Skewness </div>", unsafe_allow_html=True)
                    st.markdown("<div> Sum </div>", unsafe_allow_html=True)
                    st.markdown("<div> Variance </div>", unsafe_allow_html=True)
                
                
                with col10:
                    st.markdown('</br>', unsafe_allow_html= True)
                    st.markdown('</br>', unsafe_allow_html= True)
                    st.markdown('</br>', unsafe_allow_html= True)
                    st.markdown('</br>', unsafe_allow_html= True)
                    st.markdown(f"<div style='color: green; font-style: italic;'</div>{round(df[column].std(), 5)}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='color: green; font-style: italic;'</div>{round(df[column].std() / df[column].mean(), 5)}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='color: green; font-style: italic;'</div>{round(kurtosis(df[column]), 5)}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='color: green; font-style: italic;'</div>{round(df[column].mean(), 5)}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='color: green; font-style: italic;'</div>{round(calculate_mad(df,column), 5)}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='color: green; font-style: italic;'</div>{round(skew(df[column]), 5)}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='color: green; font-style: italic;'</div>{round(df[column].sum(), 5)}</div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='color: green; font-style: italic;'</div>{round(df[column].var(), 5)}</div>", unsafe_allow_html=True)
                  
                         
        with tab2:
            st.markdown('</br>', unsafe_allow_html=True)
            tab7, tab8 = st.tabs(['Histogram', 'Dynamic Histogram'])
            with tab7:
                df_filtered = df[~df[column].isna()]
                fig_fixed = go.Figure(data=[go.Histogram(x=df_filtered[column], nbinsx=10)])
                fig_fixed.update_layout(
                    title=f'Histogram of {column}',
                    xaxis_title=column,
                    yaxis_title='Frequency',
                    showlegend=False,
                )
                st.plotly_chart(fig_fixed)
                st.markdown("<p style='text-align: center;'><b>Histogram with fixed size bins</b> (bins=10)</p>", unsafe_allow_html=True)
            
            
            with tab8:
                hist, bins = np.histogram(df_filtered[column], bins='auto')
                bin_edges = bayesian_blocks(df_filtered[column])

                fig_dynamic = go.Figure(data=[go.Histogram(x=df_filtered[column], xbins=dict(start=min(bin_edges), end=max(bin_edges), size=bin_edges))])
                fig_dynamic.update_layout(
                    title=f'Dynamic histogram of {column}',
                    xaxis_title=column,
                    yaxis_title='Frequency',
                    showlegend=False,
                )
                st.plotly_chart(fig_dynamic)
                st.markdown("<div style='text-align: center;'><b>Histogram with variable size bins</b> (using Bayesian Blocks binning strategy)</div>", unsafe_allow_html=True)

                
                
        with tab3:
            col1, col2, col3, col4 = st.columns(([1,1,1,3]))
            with col1:
                st.markdown("<b>Value</b>", unsafe_allow_html=True)
                top_values_counts = value_count(df, column)
                for value, count in top_values_counts.items():
                    st.markdown(f"<div ><b>{value}<b></div>", unsafe_allow_html=True)
            with col2:
                st.markdown("<b>Count</b>", unsafe_allow_html=True)
                for value, count in top_values_counts.items():
                    st.markdown(f"<div style='color: green; font-style: italic;'>{count}</div>", unsafe_allow_html=True)    
            with col3:
                st.markdown("<b>Frequency (%)</b>", unsafe_allow_html=True)
                for value, count in top_values_counts.items():
                    percentage = round(count * 100/len(df[column]),1)
                    st.markdown(f"<div style='color: green; font-style: italic;'>{percentage}%</div>", unsafe_allow_html=True)
                    
            with col4:
                st.bar_chart(top_values_counts)
                   
            
        with tab4:
            st.markdown("</br>", unsafe_allow_html=True)
            tab1 , tab2 = st.tabs(["Minimum 5 values", "Maximum 5 values"])
            with tab1:
                col1 , col2, col3, col4 = st.columns([1,1,1,3])
                with col1:
                    st.markdown("<b>Value</b>", unsafe_allow_html=True)
                    min_values_counts = find_min_values(df, column)
                    for value in min_values_counts:
                        st.markdown(f"<b>{value}</b>", unsafe_allow_html=True)
                with col2:
                    st.markdown("<b>Count</b>", unsafe_allow_html=True)
                    for value, count in min_values_counts.items():
                        st.markdown(f"<span style='color: green; font-style: italic;'>{count}", unsafe_allow_html=True)
                with col3:
                    st.markdown("<b>Frequency (%)</b>", unsafe_allow_html=True)
                    for value, count in min_values_counts.items():
                        percentage = round(count * 100/len(df[column]),1)
                        st.markdown(f"<span style='color: green; font-style: italic;'>{percentage}%", unsafe_allow_html=True)
                with col4:
                    st.bar_chart(min_values_counts)
            
            with tab2:
                
                col1 , col2, col3, col4 = st.columns([1,1,1,3])
                with col1:
                    st.markdown("<b>Value</b>", unsafe_allow_html=True)
                    max_values_counts = find_max_values(df, column)
                    for value in max_values_counts:
                        st.markdown(f"<b>{value}</b>", unsafe_allow_html=True)
                with col2:
                    st.markdown("<b>Count</b>", unsafe_allow_html=True)
                    for value, count in max_values_counts.items():
                        st.markdown(f"<span style='color: green; font-style: italic;'>{count}", unsafe_allow_html=True)
                with col3:
                    st.markdown("<b>Frequency (%)</b>", unsafe_allow_html=True)
                    for value, count in max_values_counts.items():
                        percentage = round(count * 100/len(df[column]),1)
                        st.markdown(f"<span style='color: green; font-style: italic;'>{percentage}%", unsafe_allow_html=True)
                with col4:
                    st.bar_chart(max_values_counts)




def categorical_column(df, column):
    col1, col2, col3, col4 = st.columns((4))
    with col1:
        column_type = categorize_column_type(df, column)
        st.markdown(f"{column_type}")
        generate_badge(df,column)         
    with col2:
        col1 , col2 = st.columns((2))
        cc = column_characteristics(df,column)
        with col1:
            if "UNIQUE" in cc:
                st.markdown('<span style="color:#aa3333;">Distinct count</span>', unsafe_allow_html=True)
                st.markdown('<span style="color:#aa3333;">Unique(%)</span>', unsafe_allow_html=True)
            else:
                st.markdown("Distinct count")
                st.markdown("Unique(%)")
            if 'MISSING' in cc:        
                st.markdown('<span style="color:#aa3333;">Missing</span>', unsafe_allow_html=True)
                st.markdown('<span style="color:#aa3333;">Missing(%)</span>', unsafe_allow_html=True)
            else:
                st.markdown("Missing")
                st.markdown("Missing (%)") 
            st.markdown("Memory size")
            
        with col2:
            st.markdown(f"<span style='color: green; font-style: italic;'>{df[column].nunique()}", unsafe_allow_html=True)
            st.markdown(f"<span style='color: green; font-style: italic;'>{round((df[column].nunique() / len(df[column])) * 100, 3) if len(df[column]) > 0 else 0}", unsafe_allow_html=True)
            st.markdown(f"<span style='color: green; font-style: italic;'>{df[column].isnull().sum()}", unsafe_allow_html=True)
            st.markdown(f"<span style='color: green; font-style: italic;'>{round((df[column].isnull().sum() / len(df[column])) * 100 ,3 ) if len(df[column]) > 0 else 0}", unsafe_allow_html=True)
            st.markdown(f"<span style='color: green; font-style: italic;'>{round(df[column].memory_usage(deep=True) / 1024, 3)} KiB", unsafe_allow_html=True)
    with col3:
        col1 , col2 = st.columns((2))
        with col1:
            pass
        with col2:
            pass
       
    with col4:
        pass



def toggle_button_for_categorical(df, column):
    unique_key = f"button_{column}"
    if 'button' not in st.session_state:
        st.session_state.button = False     

    st.button('Toggle details', key=unique_key, on_click=click_button)

    if st.session_state.button:
        tab1, tab2 , tab3 = st.tabs(['Common values', 'Length', 'Character'])
        with tab1:
            col1, col2, col3, col4 = st.columns(([2,1,1,2]))
            with col1:
                st.markdown("<b>Value</b>", unsafe_allow_html=True)
                top_values_counts = value_count(df, column)
                for value, count in top_values_counts.items():
                    st.markdown(f"<div >{value}</div>", unsafe_allow_html=True)
            with col2:
                st.markdown("<b>Count</b>", unsafe_allow_html=True)
                for value, count in top_values_counts.items():
                    st.markdown(f"<div style='color: green; font-style: italic;'>{count}</div>", unsafe_allow_html=True)    
            with col3:
                st.markdown("<b>Frequency (%)</b>", unsafe_allow_html=True)
                for value, count in top_values_counts.items():
                    percentage = round(count * 100/len(df[column]),1)
                    st.markdown(f"<div style='color: green; font-style: italic;'>{percentage}%</div>", unsafe_allow_html=True)
                    
            with col4:
                st.bar_chart(top_values_counts)
        
        
        with tab2:
            col1, col2,col3 = st.columns((3))
            with col1:
                st.markdown("<b> Length </b>", unsafe_allow_html= True)
                st.markdown("</br>", unsafe_allow_html=True)
                st.markdown("<b>Max length </b>", unsafe_allow_html=True)
                st.markdown("<b> Mean length </b>", unsafe_allow_html=True)
                st.markdown("<b> Min length </b>", unsafe_allow_html=True)
            with col2:
                st.markdown("</br>", unsafe_allow_html=True)
                st.markdown("</br>", unsafe_allow_html=True)
                st.markdown("</br>", unsafe_allow_html=True)
                st.markdown(f"<span style='color: green; font-style: italic;'>{df[column].str.len().max()}</span>", unsafe_allow_html=True)
                st.markdown(f"<span style='color: green; font-style: italic;'>{round(df[column].str.len().mean(),3)}</span>", unsafe_allow_html=True)
                st.markdown(f"<span style='color: green; font-style: italic;'>{df[column].str.len().min()}</span>", unsafe_allow_html=True)
                
            with col3:                
                max_length, mean_length, min_length = calculate_length_metrics(df,column)

                # Calculate frequency of each length category
                length_metrics = {
                    'Max Length': max_length,
                    'Mean Length': mean_length,
                    'Min Length': min_length
                }
                length_counts = df[column].str.len().value_counts().sort_index()
                data_dict = {metric: length_counts[length] if length in length_counts.index else 0 for metric, length in length_metrics.items()}

                st.bar_chart(data_dict)
        
        
        with tab3:
            col_1, col_2, col_3, col_4 = st.columns((4))
            with col_1:
                st.markdown("<b> Value </b>", unsafe_allow_html= True)
                counts = character_count_from_df(df, column)
                for category, count in counts.items():
                    if count > 0:
                        st.write(category.replace('_', ' '))
                         
            with col_2:
                st.markdown("<b> Count </b>", unsafe_allow_html= True)
                for category, count in counts.items():
                    if count > 0:
                        st.write(f"<span style='color: green; font-style: italic;'>{count}", unsafe_allow_html=True)
            
            with col_3:
                st.markdown("<b> Frequency </b>", unsafe_allow_html= True)
                total_characters = sum(counts.values())
                for category, count in counts.items():
                    if count > 0:
                        percentage = round(count * 100 / total_characters, 3)
                        st.write(f"<span style='color: green; font-style: italic;'>{percentage}%</span>", unsafe_allow_html=True)                
                               
                        
                            
                                    
def boolean_column(df,column):
    col1, col2, col3, col4 = st.columns((4))
    with col1:
        column_type = categorize_column_type(df, column)
        st.markdown(f"{column_type}")
        generate_badge(df,column)
        cc = column_characteristics(df, column)         
    with col2:
        col1 , col2 = st.columns((2))
        with col1:
            if "UNIQUE" in cc:
                st.markdown('<span style="color:#aa3333;">Distinct count</span>', unsafe_allow_html=True)
                st.markdown('<span style="color:#aa3333;">Unique(%)</span>', unsafe_allow_html=True)
            else:
                st.markdown("Distinct count")
                st.markdown("Unique(%)")
            if 'MISSING' in cc:        
                st.markdown('<span style="color:#aa3333;">Missing</span>', unsafe_allow_html=True)
                st.markdown('<span style="color:#aa3333;">Missing(%)</span>', unsafe_allow_html=True)
            else:
                st.markdown("Missing")
                st.markdown("Missing (%)") 
            st.markdown("Memory size")
            
        with col2:
            st.markdown(f"<span style='color: green; font-style: italic;'>{df[column].nunique()}", unsafe_allow_html=True)
            st.markdown(f"<span style='color: green; font-style: italic;'>{round((df[column].nunique() / len(df[column])) * 100, 3) if len(df[column]) > 0 else 0}", unsafe_allow_html=True)
            st.markdown(f"<span style='color: green; font-style: italic;'>{df[column].isnull().sum()}", unsafe_allow_html=True)
            st.markdown(f"<span style='color: green; font-style: italic;'>{round((df[column].isnull().sum() / len(df[column])) * 100 ,3 ) if len(df[column]) > 0 else 0}", unsafe_allow_html=True)
            st.markdown(f"<span style='color: green; font-style: italic;'>{round(df[column].memory_usage(deep=True) / 1024, 3)} KiB", unsafe_allow_html=True)
    with col3:
        col1 , col2 = st.columns((2))
        with col1:
            pass
        with col2:
            pass
       
    with col4:
        pass


def toggle_button_for_boolean(df, column):
    unique_key = f"button_{column}"
    if 'button' not in st.session_state:
        st.session_state.button = False     

    st.button('Toggle details', key=unique_key, on_click=click_button)

    if st.session_state.button:
        tab1, tab2 = st.tabs(["Frequency Table", "Histogram"])
        with tab1:
            col1, col2, col3, col4 = st.columns(([1,1,1,2]))
            with col1:
                st.markdown("<b>Value</b>", unsafe_allow_html=True)
                top_values_counts = value_count(df, column)
                for value, count in top_values_counts.items():
                    st.markdown(f"<div ><b>{value}<b></div>", unsafe_allow_html=True)
            with col2:
                st.markdown("<b>Count</b>", unsafe_allow_html=True)
                for value, count in top_values_counts.items():
                    st.markdown(f"<div style='color: green; font-style: italic;'>{count}</div>", unsafe_allow_html=True)
            with col3:
                st.markdown("<b>Frequency (%)</b>", unsafe_allow_html=True)
                for value, count in top_values_counts.items():
                    percentage = round(count * 100/len(df[column]),1)
                    st.markdown(f"<div style='color: green; font-style: italic;'>{percentage}%</div>", unsafe_allow_html=True)
            with col4:
                st.bar_chart(top_values_counts)
        
        with tab2: 
            fig = px.histogram(df, x=df[column], nbins=2, labels={'boolean_column': 'Boolean Values', 'count': 'Frequency'})
            st.plotly_chart(fig)                             



def datetime_column(df,column):
    col7 , col8, col9 , col10= st.columns((4))
    with col7:
        column_type = categorize_column_type(df, column)
        st.markdown(f"{column_type}")
        generate_badge(df,column)   
        cc = column_characteristics(df,column)      
    with col8:
        col1 , col2 = st.columns((2))
        with col1:
            if "UNIQUE" in cc:
                st.markdown('<span style="color:#aa3333;">Distinct count</span>', unsafe_allow_html=True)
                st.markdown('<span style="color:#aa3333;">Unique(%)</span>', unsafe_allow_html=True)
            else:
                st.markdown("Distinct count")
                st.markdown("Unique(%)")
            if 'MISSING' in cc:        
                st.markdown('<span style="color:#aa3333;">Missing</span>', unsafe_allow_html=True)
                st.markdown('<span style="color:#aa3333;">Missing(%)</span>', unsafe_allow_html=True)
            else:
                st.markdown("Missing")
                st.markdown("Missing (%)") 
            st.markdown("Memory size")
            
        with col2:
            st.markdown(f"<span style='color: green; font-style: italic;'>{df[column].nunique()}", unsafe_allow_html=True)
            st.markdown(f"<span style='color: green; font-style: italic;'>{round((df[column].nunique() / len(df[column])) * 100, 3) if len(df[column]) > 0 else 0}", unsafe_allow_html=True)
            st.markdown(f"<span style='color: green; font-style: italic;'>{df[column].isnull().sum()}", unsafe_allow_html=True)
            st.markdown(f"<span style='color: green; font-style: italic;'>{round((df[column].isnull().sum() / len(df[column])) * 100 ,3 ) if len(df[column]) > 0 else 0}", unsafe_allow_html=True)
            st.markdown(f"<span style='color: green; font-style: italic;'>{round(df[column].memory_usage(deep=True) / 1024, 3)} KiB", unsafe_allow_html=True)
    with col9:
        col1 , col2 = st.columns((2))
        with col1:
            st.markdown("Minimum")
            st.markdown("Maximum")
        with col2:
            if df[column].dtype == 'object':
                df[column] = pd.to_datetime(df[column])
            st.markdown(f"<span style='color: green; font-style: italic;'>{df[column].min()}", unsafe_allow_html=True)
            st.markdown(f"<span style='color: green; font-style: italic;'>{df[column].max()}", unsafe_allow_html=True)    
                    
    with col10:
        pass       



def toggle_button_for_datetime(df, column):
    unique_key = f"button_{column}"
    if 'button' not in st.session_state:
        st.session_state.button = False     

    st.button('Toggle details', key=unique_key, on_click=click_button)

    if st.session_state.button:
        st.markdown('Histogram')
        st.markdown('</br>', unsafe_allow_html=True)
        fig = px.histogram(df, x=df[column], labels={'datetime_column': 'Datetime Values', 'count': 'Frequency'})
        st.plotly_chart(fig)
                    
        
        
def create_expander(df,column_name):
        with st.expander(column_name):
            if categorize_column_type(df,column_name) == "numeric":
                numerical_column(df,column_name)
                toggle_button_for_numeric(df,column_name)
            elif categorize_column_type(df,column_name) == "datetime":
                datetime_column(df,column_name)
                toggle_button_for_datetime(df,column_name)     
            elif categorize_column_type(df,column_name) == "categorical":
                categorical_column(df,column_name)
                toggle_button_for_categorical(df,column_name)
            elif categorize_column_type(df,column_name) == "boolean":
                boolean_column(df,column_name)
                toggle_button_for_boolean(df,column_name)
                        
            
             


def variable_main(df):    
    st.markdown('## Variables')
    st.markdown('---')
    for column in df.columns:
        create_expander(df,column)