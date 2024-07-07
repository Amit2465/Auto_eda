import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder


def custom_css_box(text):    
    custom_css = f"""
    <style>
        .custom-box {{
            background-color: #F0F2F6;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 0 8px rgba(0, 0, 0, 0.1);
        }}
    </style>
    """
    # Display the custom-styled box with content
    st.markdown(custom_css, unsafe_allow_html=True)
    st.markdown(f'<div class="custom-box">{text}</div>', unsafe_allow_html=True)


# This is a function for sample section
def sample_dataframe(df):
    st.markdown('### Sample')
    
    sample_text = """
    The Sample section shows you the beginning and end of your uploaded dataset. 
    It displays the first 10 rows and the last 10 rows, giving you a quick overview 
    of the dataset’s structure and content.
    """
    custom_css_box(sample_text)

    
    st.markdown('<br>', unsafe_allow_html=True)
    if df is not None:
        st.markdown('## First rows :arrow_up:')
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_grid_options(domLayout='autoHeight')
        grid_options = gb.build()
        AgGrid(df.head(10), gridOptions=grid_options, fit_columns_on_grid_load=True)         
        st.markdown('## Last rows :arrow_down:')
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_grid_options(domLayout='autoHeight')
        grid_options = gb.build()        
        AgGrid(df.tail(10), gridOptions=grid_options, fit_columns_on_grid_load=True)
        
        
    