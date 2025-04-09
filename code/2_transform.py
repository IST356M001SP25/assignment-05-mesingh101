import pandas as pd
import streamlit as st
import pandaslib as pl

# TODO: Write your transformation code here

from pandaslib import clean_currency, clean_country_usa, extract_year_mdy

# Load data
survey_data = pd.read_csv('cache/survey.csv')
states_data = pd.read_csv('cache/states.csv')

# Load COL data by year
col_dataframes = []
cols = []  # Make sure this is defined BEFORE the loop

for year in survey_data['year'].dropna().unique():
    try:
        year = int(year)
        col = pd.read_csv(f'cache/col_{year}.csv')
        cols.append(col)
    except FileNotFoundError:
        print(f"[Warning] COL file missing for year {year}")


col_data = pd.concat(col_dataframes, ignore_index=True)

# Clean country field
survey_data['_country'] = survey_data['What country do you work in?'].apply(clean_country_usa)

# Join with states data to get abbreviations
survey_states_combined = survey_data.merge(
    states_data,
    left_on="If you're in the U.S., what state do you work in?",
    right_on='State',
    how='inner'
)

# Create full city name for joining with COL data
survey_states_combined['_full_city'] = (
    survey_states_combined['What city do you work in?'] + ', ' +
    survey_states_combined['Abbreviation'] + ', ' +
    survey_states_combined['_country']
)

# Merge with COL data
combined = survey_states_combined.merge(
    col_data,
    left_on=['year', '_full_city'],
    right_on=['year', 'full_city'],
    how='inner'
)

# Clean and adjust salary
combined["_annual_salary_cleaned"] = combined['What is your annual base salary?'].apply(clean_currency)
combined["_annual_salary_adjusted"] = combined.apply(
    lambda row: row["_annual_salary_cleaned"] * (100 / row["Cost of Living Index"]), axis=1
)

# Save full engineered dataset
combined.to_csv('cache/survey_dataset.csv', index=False)

# Generate reports
report_age = combined.pivot_table(
    index='_full_city',
    columns='How old are you?',
    values='_annual_salary_adjusted',
    aggfunc='mean'
)
report_age.to_csv('cache/annual_salary_adjusted_by_location_and_age.csv')

report_edu = combined.pivot_table(
    index='_full_city',
    columns='What is your highest level of education?',
    values='_annual_salary_adjusted',
    aggfunc='mean'
)
report_edu.to_csv('cache/annual_salary_adjusted_by_location_and_education.csv')
