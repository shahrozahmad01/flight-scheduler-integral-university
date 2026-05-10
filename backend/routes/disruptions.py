from flask import Blueprint, request, jsonify
from models.disruption import Disruption
from services.disruption_handler import DisruptionHandler
from services.impact_analyser import ImpactAnalyser
from services.notification_service import NotificationService


disruptions_bp = Blueprint('disruptions_bp', __name__, url_prefix='/api/disruptions')


@disruptions_bp.route('/', methods=['GET'])
def list_disruptions():
    disruptions = Disruption.query.order_by(Disruption.reported_at.desc()).all()
    return jsonify([d.to_dict() for d in disruptions])


@disruptions_bp.route('/trigger', methods=['POST'])
def trigger_disruption():
    data = request.get_json() or {}
    required = ['flight_id', 'disruption_type', 'reason']
    if not all(key in data for key in required):
        return jsonify({'error': 'Missing required fields'}), 400

    disruption = DisruptionHandler.trigger_disruption(
        flight_id=data['flight_id'],
        disruption_type=data['disruption_type'],
        reason=data['reason'],
        delay_minutes=data.get('delay_minutes', 0),
    )
    if not disruption:
        return jsonify({'error': 'Unable to create disruption'}), 500

    notifications = NotificationService.send_bulk_notifications(data['flight_id'], disruption)
    result = disruption.to_dict()
    result['notifications_sent'] = len(notifications)
    return jsonify(result), 201


@disruptions_bp.route('/<int:disruption_id>/affected', methods=['GET'])
def affected_passengers(disruption_id):
    disruption = Disruption.query.get(disruption_id)
    if not disruption:
        return jsonify({'error': 'Disruption not found'}), 404
    rows = DisruptionHandler.get_affected_passengers(disruption.flight_id)
    return jsonify(rows)


@disruptions_bp.route('/<int:disruption_id>/analysis', methods=['GET'])
def disruption_analysis(disruption_id):
    disruption = Disruption.query.get(disruption_id)
    if not disruption:
        return jsonify({'error': 'Disruption not found'}), 404
    summary = ImpactAnalyser.analyse_flight_disruption(disruption.flight_id)
    return jsonify(summary)


@disruptions_bp.route('/<int:disruption_id>/resolve', methods=['PUT'])
def resolve_disruption(disruption_id):
    disruption = DisruptionHandler.resolve_disruption(disruption_id)
    if not disruption:
        return jsonify({'error': 'Unable to resolve disruption'}), 500
    return jsonify(disruption.to_dict())
