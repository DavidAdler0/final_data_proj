import os
import folium
from flask import Blueprint, render_template, request, make_response

from repositories.map_repository import generate_map_lethality_by_area, generate_map_lethality_pct_change, \
    generate_map_active_groups, generate_map_targeted_locations

map_bp = Blueprint('map', __name__)

def no_cache(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response
@map_bp.route('/', methods=['GET'])
def home():
    response = make_response(render_template('home.html'))
    return no_cache(response), 200
@map_bp.route('/render_map', methods=['GET', 'POST'])
def render_map():
    try:
        response = make_response(render_template('map.html'))
        return no_cache(response), 200
    except Exception as e:
        return f"an error occured: {e}"

@map_bp.route("/submit", methods=["GET", "POST"])
def submit():
    try:
        # Capture input from the user's HTML Form
        query = request.form['query']
        area = request.form['area_type']
        region = request.form['region']
        input1 = request.form['input_1']
        input2 = request.form['input_2']

        success = None
        match query:
            case "1":
                success = generate_map_lethality_by_area(area)
            case "2":
                success = generate_map_lethality_pct_change()
            case "3":
                success = generate_map_active_groups(area)
            case "4":
                success = generate_map_targeted_locations()
        if success:
            response = make_response(render_template("index.html"))
            return no_cache(response), 200
        return "an error occurred while generating the map", 500
    except Exception as e:
        return f"an error occured: {e}", 500