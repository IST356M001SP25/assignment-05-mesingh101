import pandas as pd
import numpy as np
import streamlit as st
import pandaslib as pl
from pandaslib import extract_year_mdy

#TODO Write your extraction code here

#Download and save the states data
states_url = "https://docs.google.com/spreadsheets/d/14wvnQygIX1eCVo7H5B7a96W1v5VCg6Q9yeRoESF6epw/export?format=csv"
states_df = pd.read_csv(states_url)
states_df.to_csv('cache/states.csv', index=False)

#Download, process, and save the survey data
survey_url = "https://docs.google.com/spreadsheets/d/1IPS5dBSGtwYVbjsfbaMCYIWnOuRmJcbequohNxCyGVw/export?resourcekey=&gid=1625408792&format=csv"
survey_df = pd.read_csv(survey_url)
survey_df['year'] = survey_df['Timestamp'].apply(extract_year_mdy)
survey_df.to_csv('cache/survey.csv', index=False)

#Download and save cost of living data for each unique year
unique_years = survey_df['year'].dropna().unique()
for year in unique_years:
    col_url = f"https://www.numbeo.com/cost-of-living/rankings.jsp?title={year}&displayColumn=cost_of_living_index"
    col_df_list = pd.read_html(col_url)
    if col_df_list:
        col_df = col_df_list[0]
        col_df['year'] = year
        col_df.to_csv(f'cache/col_{year}.csv', index=False)
