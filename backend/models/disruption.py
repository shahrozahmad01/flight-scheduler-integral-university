from datetime import datetime
from database import db


class Disruption(db.Model):
    __tablename__ = 'disruptions'

    id = db.Column(db.Integer, primary_key=True)
    flight_id = db.Column(db.Integer, db.ForeignKey('flights.id'), nullable=False)
    disruption_type = db.Column(db.String(20), nullable=False)
    reason = db.Column(db.String(200), nullable=False)
    reported_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved = db.Column(db.Boolean, default=False)
    passengers_affected = db.Column(db.Integer, default=0)
    passengers_rebooked = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'flight_id': self.flight_id,
            'disruption_type': self.disruption_type,
            'reason': self.reason,
            'reported_at': self.reported_at.isoformat(),
            'resolved': self.resolved,
            'passengers_affected': self.passengers_affected,
            'passengers_rebooked': self.passengers_rebooked,
            'flight_number': self.flight.flight_number if self.flight else None,
        }

    def __repr__(self):
        return f'<Disruption {self.disruption_type} flight={self.flight_id}>'
