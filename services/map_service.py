import folium
import requests
from sqlalchemy.testing.exclusions import succeeds_if

from services.analysis_service import lethality_avg_by_area, most_targeted_location_by_area
from services.geojson_service import generate_geojson_with_pct_change, generate_geojson_with_active_groups


def generate_map_lethality_by_area(area):
    lethality_by_area = lethality_avg_by_area(area)

    # to_do: other area options
    url = "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/world_countries.json"
    geo_data = requests.get(url).json()

    m = folium.Map(location=[0, 0], zoom_start=2)

    folium.Choropleth(
        geo_data=geo_data,
        name='choropleth',
        data=lethality_by_area,
        columns=[area, 'lethality_level'],
        key_on='feature.properties.name',
        fill_color='YlOrRd',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Terrorism Index',
        bins=[0, 1, 25, 50, 75, 100, 250],
        nan_fill_color='white',
        nan_fill_opacity=0.7
    ).add_to(m)

    folium.LayerControl().add_to(m)

    m.save("templates/map1.html")
    print("saved new map1")
    return True


def generate_map_lethality_pct_change(area=None):
    try:
        world_geo = generate_geojson_with_pct_change()
        if world_geo is None:
            raise ValueError("Failed to generate GeoJSON. The data might be missing or invalid.")

        for feature in world_geo['features']:
            if 'lethality_change_by_year' not in feature['properties']:
                feature['properties']['lethality_change_by_year'] = "No data available"

        m = folium.Map([0, 0], zoom_start=2)

        popup = folium.GeoJsonPopup(
            fields=["name", "lethality_change_by_year"],
            aliases=["Country Name", "Lethality Change by Year"],
            empty_label="No data available"
        )

        folium.GeoJson(
            world_geo,
            highlight_function=lambda feature: {
                "fillColor": "green",
                "color": "black",
                "weight": 2,
                "fillOpacity": 0.6
            },
            popup=popup,
            popup_keep_highlighted=True,
        ).add_to(m)

        m.save("templates/map2.html")
        print("Saved new map to templates/map2.html")
        return True

    except ValueError as ve:
        print(f"ValueError: {ve}")
        return False

    except KeyError as ke:
        print(f"KeyError: {ke}")
        return False

    except IOError as ioe:
        print(f"IOError: {ioe}")
        return False

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

def generate_map_active_groups(area="country"):
    try:
        world_geo = generate_geojson_with_active_groups()
        if world_geo is None:
            raise ValueError("Failed to generate GeoJSON. The data might be missing or invalid.")

        for feature in world_geo['features']:
            if 'active_groups' not in feature['properties']:
                feature['properties']['active_groups'] = "No data available"


        m = folium.Map([0, 0], zoom_start=2)

        popup = folium.GeoJsonPopup(
            fields=["name", "active_groups"],
            aliases=["Country Name", "most active groups"],
            empty_label="No data available"
        )

        folium.GeoJson(
            world_geo,
            highlight_function=lambda feature: {
                "fillColor": "green",
                "color": "black",
                "weight": 2,
                "fillOpacity": 0.6
            },
            popup=popup,
            popup_keep_highlighted=True,
        ).add_to(m)

        m.save("templates/map3.html")
        print("Saved new map to templates/map3.html")
        return True

    except ValueError as ve:
        print(f"ValueError: {ve}")
        return False

    except KeyError as ke:
        print(f"KeyError: {ke}")
        return False

    except IOError as ioe:
        print(f"IOError: {ioe}")
        return False

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

def generate_map_targeted_locations(area="country"):
    df = most_targeted_location_by_area()
    m = folium.Map(location=[0, 0], zoom_start=2)

    for _, row in df.iterrows():
        popup_text = f"Country: {row['country']}\nCity: {row['city']}\nLongitude: {row['longitude']}\nLatitude: {row['latitude']}\nGroups count:{row['groups_count']}\nGroups:{row['terror_groups']}"
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=popup_text
        ).add_to(m)
    m.save("templates/map4.html")
    print("Saved new map to templates/map4.html")
    return True