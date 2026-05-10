import random
import string
from datetime import datetime
from database import db


class Passenger(db.Model):
    __tablename__ = 'passengers'

    id = db.Column(db.Integer, primary_key=True)
    pnr = db.Column(db.String(6), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(15))
    tier = db.Column(db.String(20), default='ECONOMY')
    frequent_flyer = db.Column(db.Boolean, default=False)
    special_needs = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    bookings = db.relationship('Booking', backref='passenger', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'pnr': self.pnr,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'tier': self.tier,
            'frequent_flyer': self.frequent_flyer,
            'special_needs': self.special_needs,
            'created_at': self.created_at.isoformat(),
        }

    def __repr__(self):
        return f'<Passenger {self.name} ({self.pnr})>'

    @staticmethod
    def generate_pnr():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
