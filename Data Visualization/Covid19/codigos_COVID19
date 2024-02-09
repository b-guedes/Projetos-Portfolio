#importar as bibliotecas que serão utilizadas
import requests

import numpy as np
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt



#abrindo o arquivo no Pandas
url = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
df_casos = pd.read_csv(url, sep=',')

  
#retirando as colunas que não interessam ao projeto
df_limpando = df_casos.drop(['icu_patients',
                             'icu_patients_per_million',
                             'hosp_patients',
                             'hosp_patients_per_million',
                             'weekly_icu_admissions',
                             'weekly_icu_admissions_per_million',
                             'weekly_hosp_admissions',
                             'weekly_hosp_admissions_per_million',
                             'reproduction_rate',
                             'total_tests',
                             'new_tests',
                             'total_tests_per_thousand',
                             'new_tests_per_thousand',
                             'new_tests_smoothed',
                             'new_tests_smoothed_per_thousand',
                             'positive_rate',
                             'tests_per_case',
                             'tests_units',
                             'extreme_poverty',
                             'population_density',
                             'stringency_index',
                             'aged_65_older',
                             'aged_70_older',
                             'total_vaccinations_per_hundred',
                             'people_vaccinated_per_hundred',
                             'people_fully_vaccinated_per_hundred',
                             'total_boosters_per_hundred',
                             'new_people_vaccinated_smoothed_per_hundred',
                             'cardiovasc_death_rate',
                             'diabetes_prevalence',
                             'female_smokers',
                             'male_smokers',
                             'handwashing_facilities',
                             'iso_code'
                             ], axis=1)

  
  #preenchendo os dados vazios
df_limpando = df_limpando.fillna(0)

  
#garantindo os tipos de cada coluna - int e datetime
df_limpando['total_cases'] = df_limpando['total_cases'].astype('int64')
df_limpando['new_cases'] = df_limpando['new_cases'].astype('int64')
df_limpando['total_deaths'] = df_limpando['total_deaths'].astype('int64')
df_limpando['new_deaths'] = df_limpando['new_deaths'].astype('int64')
df_limpando['total_vaccinations'] = df_limpando['total_vaccinations'].astype('int64')
df_limpando['people_vaccinated'] = df_limpando['people_vaccinated'].astype('int64')
df_limpando['people_fully_vaccinated'] = df_limpando['people_fully_vaccinated'].astype('int64')
df_limpando['total_boosters'] = df_limpando['total_boosters'].astype('int64')
df_limpando['new_vaccinations'] = df_limpando['new_vaccinations'].astype('int64')
df_limpando['date'] = df_limpando['date'].astype('datetime64[ns]')
df_limpando['population'] = df_limpando['population'].astype('int64')

#garantindo os tipos de cada coluna - float - e o arredondamento correto
df_limpando['new_cases_smoothed'] = df_limpando['new_cases_smoothed'].astype('float64').round(3)
df_limpando['new_deaths_smoothed'] = df_limpando['new_deaths_smoothed'].astype('float64').round(3)
df_limpando['total_cases_per_million'] = df_limpando['total_cases_per_million'].astype('float64').round(3)
df_limpando['new_cases_per_million'] = df_limpando['new_cases_per_million'].astype('float64').round(3)
df_limpando['new_cases_smoothed_per_million'] = df_limpando['new_cases_smoothed_per_million'].astype('float64').round(3)
df_limpando['total_deaths_per_million'] = df_limpando['total_deaths_per_million'].astype('float64').round(3)
df_limpando['new_deaths_per_million'] = df_limpando['new_deaths_per_million'].astype('float64').round(3)
df_limpando['new_deaths_smoothed_per_million'] = df_limpando['new_deaths_smoothed_per_million'].astype('float64').round(3)
df_limpando['new_vaccinations_smoothed'] = df_limpando['new_vaccinations_smoothed'].astype('float64').round(3)
df_limpando['new_vaccinations_smoothed_per_million'] = df_limpando['new_vaccinations_smoothed_per_million'].astype('float64').round(3)
df_limpando['new_people_vaccinated_smoothed'] = df_limpando['new_people_vaccinated_smoothed'].astype('float64').round(3)
df_limpando['gdp_per_capita'] = df_limpando['gdp_per_capita'].astype('float64').round(3)
df_limpando['hospital_beds_per_thousand'] = df_limpando['hospital_beds_per_thousand'].astype('float64').round(3)
df_limpando['life_expectancy'] = df_limpando['life_expectancy'].astype('float64').round(2)
df_limpando['human_development_index'] = df_limpando['human_development_index'].astype('float64').round(3)
df_limpando['excess_mortality_cumulative_absolute'] = df_limpando['excess_mortality_cumulative_absolute'].astype('float64').round(3)
df_limpando['excess_mortality_cumulative'] = df_limpando['excess_mortality_cumulative'].astype('float64').round(3)
df_limpando['excess_mortality'] = df_limpando['excess_mortality'].astype('float64').round(3)
df_limpando['excess_mortality_cumulative_per_million'] = df_limpando['excess_mortality_cumulative_per_million'].astype('float64').round(4)


#criar um Dataset para América do Sul, excluindo local
df_limpo_AS = df_limpando.query(
    'continent == "South America" & location != "Falkland Islands"'
    ).reset_index(drop=True)


#Criando dataset para o G20, selecionando países de interesse e retirando mais algumas colunas
df_limpo_G20 = df_limpando.query(
    'location == "Brazil" | location == "Argentina" | '
    'location == "United States" | location == "Canada" | '
    'location == "Mexico" | location == "China" | '
    'location == "Japan" | location == "South Korea" | '
    'location == "India" | location == "Turkey" | '
    'location == "Saudi Arabia" | location == "Indonesia" | '
    'location == "Germany" | location == "France" | '
    'location == "Italy" | location == "Russia" | '
    'location == "United Kingdom" | location == "South Africa" | '
    'location == "Australia"'
).reset_index(drop=True)


#criar um arquivo CSV para ser exportado
df_limpo_AS.to_csv('./covid-AmericaSul.csv', sep=',', index=False)
df_limpo_G20.to_csv('./covid-G20.csv', sep=',', index=False)

print("arquivo pronto")
