import os
import time

import folium
from flask import Blueprint, render_template, request, make_response

from services.map_service import generate_map_lethality_by_area, generate_map_lethality_pct_change, \
    generate_map_active_groups, generate_map_targeted_locations

map_bp = Blueprint('map', __name__)


@map_bp.route('/', methods=['GET'])
def home():
    m = folium.Map(location=[0, 0], zoom_start=2)
    m.save("templates/map.html")
    response = make_response(render_template('home.html'))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response, 200


@map_bp.route('/render_map', methods=['GET', 'POST'])
def render_map():
    try:
        response = make_response(render_template('map.html'))
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    except Exception as e:
        return f"an error occurred: {e}"


@map_bp.route("/submit", methods=["GET", "POST"])
def submit():
    try:

        query = request.form['query']
        area = request.form['area_type']
        region = request.form['region']
        input1 = request.form['input_1']
        input2 = request.form['input_2']

        if os.path.exists("C:/Users/adler/PycharmProjects/proj_data/templates/map.html"):
            os.remove("C:/Users/adler/PycharmProjects/proj_data/templates/map.html")
            print("removed successfully")
        success = None
        match query:
            case "1":
                success = generate_map_lethality_by_area(area)
                response = make_response(render_template('map1.html'))

            case "2":
                success = generate_map_lethality_pct_change()
                response = make_response(render_template('map2.html'))

            case "3":
                success = generate_map_active_groups(area)
                response = make_response(render_template('map3.html'))

            case "4":
                success = generate_map_targeted_locations()
                response = make_response(render_template('map4.html'))


        if success:
            print(success)
            # response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
            # response.headers["Pragma"] = "no-cache"
            # response.headers["Expires"] = "0"
            return response  # רק מחזיר את המפה המעודכנת
        return "an error occurred while generating the map", 500
    except Exception as e:
        return f"an error occurred: {e}", 500