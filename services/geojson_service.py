import requests
from services.analysis_service import lethality_change_by_area_and_year, active_groups_by_area

import json
import requests

import requests


def generate_geojson_with_pct_change():

    df = lethality_change_by_area_and_year('country')


    required_columns = {'country', 'year', 'pct_change'}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"DataFrame is missing required columns: {required_columns - set(df.columns)}")


    url = "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/world_countries.json"
    try:
        world_geo = requests.get(url).json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching GeoJSON: {e}")
        return None

    country_dict = {name: group for name, group in df.groupby('country')}

    for feature in world_geo['features']:
        country_name = feature['properties']['name']
        if country_name in country_dict:
            country_data = country_dict[country_name]
            feature['properties']['lethality_change_by_year'] = [
                {row['year']: f"{round(row['pct_change'], 2)}%"} for _, row in country_data.iterrows()
            ]

    print("Function execution completed successfully.")
    return world_geo

import requests

def generate_geojson_with_active_groups():
    df = active_groups_by_area("country", 5)

    url = "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/world_countries.json"
    try:
        world_geo = requests.get(url).json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching GeoJSON: {e}")
        return None

    country_groups = {
        country: group for country, group in df.groupby('country')
    }

    for feature in world_geo['features']:
        country_name = feature['properties']['name']
        if country_name in country_groups:
            country_data = country_groups[country_name]
            feature['properties']['active_groups'] = [
                {"group": row['terror_group'], "lethality_level": row['lethality_level']}
                for _, row in country_data.iterrows()
            ]
        else:
            feature['properties']['active_groups'] = []

    print("Function execution completed successfully.")
    return world_geo
