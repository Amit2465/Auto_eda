import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu 
import Correlations
import Sample
import Missing_Values
import Interactions
import Variables
import Overview
from Sample import custom_css_box


# setting up page configuration
st.set_page_config(
    page_title="AutoEDA",
    page_icon="clipboard-data-fill",
    layout='wide'
)


# set title and description of the page
st.title('AutoEDA :chart_with_upwards_trend:')
st.markdown('<style>div.block-container{padding-top:2rem} </style>', unsafe_allow_html=True)
text = """This app simplifies exploratory data analysis (EDA). Upload your dataset to automatically
            uncover insights, visualize patterns, and detect anomalies. EDA is crucial for understanding datasets
            through statistical graphics and visual methods, helping you gain deeper insights and validate
            assumptions about your data.
         """
custom_css_box(text)         
         

st.markdown("</br>", unsafe_allow_html= True)
st.markdown("</br>", unsafe_allow_html= True)
sample_dataset = ["Weather","Titanic","california housing","Meta",] 
ds = st.selectbox("Select a Sample Dataset", sample_dataset) 
test_data = pd.read_csv(f'Sample Datasets/{ds}.csv')

# upload data
file = st.file_uploader('Upload Dataset', type=['csv', 'xlsx'])

# Check if file is uploaded
def check_file(file):
    data = None
    try:
        if file is not None:
            # Get file name
            file_name = file.name.lower()
            # Check file extension
            if file_name.endswith('.csv'):
                data = pd.read_csv(file)
            elif file_name.endswith('.xlsx'):
                data = pd.read_excel(file)
            else:
                st.warning('Please upload a valid file format (CSV or Excel)')
                st.stop()  
    except Exception as e:
        st.write(f"Error: {str(e)}")
    return data

      
        

# Call function to check file format and create DataFrame
data = check_file(file)
if data is None:
    data = test_data
else:
    st.success('File uploaded successfully')
   
st.caption('Note: Supported file formats: csv, xlsx')
st.markdown('---')


selected = option_menu(
    menu_title=None,
    options=['Overview', 'Variables', 'Interactions', 'Correlations', 'Missing Values', 'Sample' ],
    icons = ['📊', '📈', '🔄', '🔗', '❌', '🔍'],
    default_index=0,
    orientation= 'horizontal',
)

  
# this is the main function

def main():
    if selected == 'Overview':
        Overview.overview_main(data)
    elif selected == 'Variables':
        Variables.variable_main(data)
    elif selected == 'Interactions':
        Interactions.interaction(data)
    elif selected == 'Correlations':
        Correlations.correlation(data)
    elif selected == 'Missing Values':
        Missing_Values.missing_values(data)
    else:
        Sample.sample_dataframe(data)
        
        
    # footer    
    st.markdown('</br>', unsafe_allow_html = True)  
    st.markdown("""
    <style>
        .badge-container {
            display: flex;
            justify-content: center;
        }
        .badge-container a {
            margin: 0 3px;  
        }
    </style>
    <hr>
    <div class="badge-container">
        <a href="https://www.linkedin.com/in/amit-yadav-674a9722b">
            <img src="https://img.shields.io/badge/-LinkedIn-306EA8?style=flat&logo=Linkedin&logoColor=white" alt="LinkedIn">
        </a>
        <a href="https://github.com/Amit2465">
            <img src="https://img.shields.io/badge/-GitHub-2F2F2F?style=flat&logo=github&logoColor=white" alt="GitHub">
        </a>
        <a href="mailto:your.amityadav23461@gmail.com.com">
            <img src="https://img.shields.io/badge/-Email-D14836?style=flat&logo=gmail&logoColor=white" alt="Email">
        </a>
    </div>
    </br>
    <div style="text-align: center;">© 2024 Amit Yadav</div>
    """, unsafe_allow_html=True)               
        
      

# Calling the main function 
if __name__ == '__main__':
    main()

