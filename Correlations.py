import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency
from Sample import custom_css_box



def cramers_v(x, y):
    confusion_matrix = pd.crosstab(x, y)
    chi2 = chi2_contingency(confusion_matrix)[0]
    n = confusion_matrix.sum().sum()
    phi2 = chi2 / n
    r, k = confusion_matrix.shape
    phi2corr = max(0, phi2 - ((k-1)*(r-1))/(n-1))
    rcorr = r - ((r-1)**2)/(n-1)
    kcorr = k - ((k-1)**2)/(n-1)
    return np.sqrt(phi2corr / min((kcorr-1), (rcorr-1)))


def cramers_v_matrix(df):
    cols = df.select_dtypes(include='object').columns
    n = len(cols)
    cv_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            cv_matrix[i, j] = cramers_v(df[cols[i]], df[cols[j]])
            cv_matrix[j, i] = cv_matrix[i, j] 
    return pd.DataFrame(cv_matrix, index=cols, columns=cols)



def correlation(df):
    st.markdown('## Correlations')
    tab1, tab2, tab3, tab4 = st.tabs(["Pearson's r", "Spearman's ρ", "Kendall's τ", "Cramér's V (φc)"])
    
    with tab1:
        st.markdown("### Pearson's r")
        col1,col2 = st.columns([1.5,1])
        with col2:
            text1 = '''The Pearson's correlation coefficient (r) is a measure of linear correlation between
                        two variables. It's value lies between -1 and +1, -1 indicating total negative linear 
                        correlation, 0 indicating no linear correlation and 1 indicating total positive linear
                        correlation. Furthermore, r is invariant under separate changes in location and scale
                        of the two variables, implying that for a linear function the angle to the x-axis does
                        not affect r.'''
            text12 = '''To calculate r for two variables X and Y, one divides the covariance of X and 
                        Y by the product of their standard deviations.'''
            custom_css_box(text1)
            custom_css_box(text12)             
        
        with col1:
            numeric_columns = df.select_dtypes(include=np.number).columns
            # Calculate Pearson correlation matrix
            corr_matrix = df[numeric_columns].corr()
            plt.figure(figsize=(min(5, len(numeric_columns)), max(4, len(numeric_columns) / 1.25)))
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, annot_kws={"fontsize": 6})
            plt.xticks(fontsize=7, rotation=45)
            plt.yticks(fontsize=7, rotation=0)
            plt.tight_layout()
            st.pyplot(plt)


    with tab2:
        st.markdown("### Spearman's ρ")
        col3 , col4 = st.columns([1.5,1])
        
        with col4:            
            text2 = '''The Spearman's rank correlation coefficient (ρ) is a measure of monotonic
                        correlation between two variables, and is therefore better in catching nonlinear 
                        monotonic correlations than Pearson's r. It's value lies between -1 and +1, -1
                        indicating total negative monotonic correlation, 0 indicating no monotonic
                        correlation and 1 indicating total positive monotonic correlation.'''
            text22 = '''To calculate ρ for two variables X and Y, one divides the covariance of 
                        the rank variables of X and Y by the product of their standard deviations.'''
            
            custom_css_box(text2)
            custom_css_box(text22)            
        
        with col3:
            corr_matrix = df[numeric_columns].corr(method = 'spearman')
            plt.figure(figsize=(min(5, len(numeric_columns)), max(4, len(numeric_columns) / 1.25)))
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1,annot_kws={"fontsize": 6})
            plt.xticks(fontsize= 7 ,rotation=45)
            plt.yticks(fontsize=7 ,rotation=0)
            st.pyplot(plt)     


    with tab3:        
        st.markdown("### Kendall's τ")
        col5, col6 = st.columns([1.5,1])
        with col6:
            text3 = '''Similarly to Spearman's rank correlation coefficient, the Kendall rank 
                        correlation coefficient (τ) measures ordinal association between two variables.
                        It's value lies between -1 and +1, -1 indicating total negative correlation,
                        0 indicating no correlation and 1 indicating total positive correlation.'''
            text33 = '''To calculate τ for two variables X and Y, one determines the number of 
                        concordant and discordant pairs of observations. τ is given by the number of 
                        concordant pairs minus the discordant pairs divided by the total number of pairs.'''
            custom_css_box(text3)
            custom_css_box(text33)
                                   
    
        with col5:  
            corr_matrix = df[numeric_columns].corr(method = 'kendall')
            plt.figure(figsize=(min(5, len(numeric_columns)), max(4, len(numeric_columns) / 1.25)))
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1,annot_kws={"fontsize": 6})
            plt.xticks(fontsize= 7 ,rotation=45)
            plt.yticks(fontsize=7 ,rotation=0)
            st.pyplot(plt)     

            
        
        with tab4:
            st.markdown('### Cramérs V (φc)')
            col9, col10 = st.columns([1.5,1])
            with col10:
                text5 = '''Cramér's V: Cramér's V is a statistical measure used to assess the 
                            association between categorical variables. It ranges from 0 to 1, where 0 
                            indicates no association, and 1 indicates a perfect association between the
                            variables. Cramér's V is particularly suited for contingency tables larger
                            than 2x2 and is derived from the chi-square statistic adjusted for table 
                            size. It provides a standardized way to quantify the strength of association
                            between categorical variables, offering insights into relationships that
                            traditional correlation measures may not capture.'''
                text55 = '''Cramér's V is widely used in fields such as social sciences, market research,
                            and epidemiology to analyze dependencies among categorical data, helping 
                            researchers and analysts understand the patterns and relationships within
                            their datasets.'''
                
                custom_css_box(text5)
                custom_css_box(text55)             
            
            with col9:
                # Calculate Cramér's V correlation matrix
                cv_matrix = cramers_v_matrix(df)
                plt.figure(figsize=(min(5, len(numeric_columns)), max(4, len(numeric_columns) / 1.25)))
                sns.heatmap(cv_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1,annot_kws={"fontsize": 6})
                plt.xticks(fontsize= 7 ,rotation=45)
                plt.yticks(fontsize=7 ,rotation=0)
                st.pyplot(plt) 
          