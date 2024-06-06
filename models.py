from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Location(db.Model):
    __tablename__ = 'ibb'

    terminal_id = db.Column(db.String(50), primary_key=True)
    town_id = db.Column(db.String(50))
    longitude = db.Column(db.String(50))
    latitude = db.Column(db.String(50))

    def __init__(self, terminal_id, town_id, longitude, latitude):
        self.terminal_id = terminal_id
        self.town_id = town_id
        self.longitude = longitude
        self.latitude = latitude

    def to_dict(self):
        return {
            'terminal_id': self.terminal_id,
            'town_id': self.town_id,
            'longitude': self.longitude,
            'latitude': self.latitude
        }
