from flask import Blueprint, jsonify, request
from services.analysis_service import terror_events_with_lethality_score

analysis_bp = Blueprint('analysis', __name__)


@analysis_bp.route('/attacks_by_lethality', methods=['GET'])
def attacks_by_lethality():
    df = terror_events_with_lethality_score()
    attacks_by_lethality = df.groupby("attack_type").sum('lethality_level').sort_values('lethality_level', ascending=False)['lethality_level']
    rows = request.args.get('rows')
    if rows is not None:
        attacks_by_lethality = attacks_by_lethality.head(int(rows))
    res = attacks_by_lethality.to_json()
    return jsonify(res), 200

@analysis_bp.route('/most_deadly_groups', methods=['GET'])
def most_deadly_groups():
    df = terror_events_with_lethality_score()
    res = (df.groupby('terror_group').sum('lethality_level')
           .sort_values('lethality_level',ascending=False)) \
            .reset_index()[['terror_group', 'lethality_level']].head().to_json(orient='records')
    return jsonify(res), 200


