#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 15:43:31 2020

@author: Roshan kumar thapa
"""
import pandas as pd 
import geopandas as gpd
import matplotlib.pyplot as plt

# #Data garb to excel export 
"""
data = pd.read_html('http://www.citypopulation.de/php/nepal-admin.php')
for population_data in data:
    print(population_data)

population_data.to_excel(r'pop.xlsx')
"""

population_data = pd.read_excel(r'pop.xlsx')
population_data = population_data[['Name','Status','PopulationCensus2011-06-22']]
population_data.rename(columns={'PopulationCensus2011-06-22': 'Population'},inplace=True)

# filter rows by values 
population_data = population_data.loc[population_data['Status'] == 'District']

# create an empty column
population_data['Districts2']=''

for index, row in population_data.iterrows():
    if '[' and ']' in row['Name']:
        start_index = row['Name'].find('[')
        end_index = row['Name'].find(']')
        population_data.loc[index, 'Districts2'] = population_data.loc[index]['Name'][start_index+1: end_index]
    else:
        population_data.loc[index, 'Districts2'] = population_data.loc[index]['Name']

population_data =population_data[['Population', 'Districts2']]
population_data.rename(columns ={'Districts2': 'District'},inplace=True)

# reading data from the shapefile
nep_districts = gpd.read_file(r'NPL_adm3.shp')
nep_districts = nep_districts[['NAME_3', 'geometry']]
nep_districts.plot()

nep_districts.rename(columns ={'NAME_3':'District'},inplace=True)

# reporjecting to projected coordinate system
nep_districts.to_crs(epsg=32645, inplace=True)

population_data.replace('Sindhupalchowk', 'Sindhupalchok',inplace=True)
population_data.replace('Chitwan', 'Chitawan',inplace=True)
population_data.replace('Tehrathum', 'Terhathum',inplace=True)
population_data.replace('Dang Deukhuri', 'Dang',inplace=True)
population_data.replace('Tanahun', 'Tanahu',inplace=True)
population_data.replace('Kapilvastu', 'Kapilbastu',inplace=True)

# to check The district ', row, 'is not in the population_data list
"""
for index, row in nep_districts['District'].iteritems():
    if row in population_data['District'].tolist():
        pass
    else:
        print('The district ', row, 'is not in the population_data list')
"""
# Create a new column and calculate area of the districts 
nep_districts['area'] = nep_districts.area/1000000

# Do an Attributes join
nep_districts = nep_districts.merge(population_data, on = 'District')

# create a population density column
nep_districts['pop_den(people/sq. km)'] = nep_districts['Population']/nep_districts['area']

# ploting
nep_districts.plot(column = 'pop_den(people/sq. km)', cmap = 'Spectral', legend=True)

# to export image of plot
plt.savefig('population_density') 