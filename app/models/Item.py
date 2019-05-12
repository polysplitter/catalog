import datetime
from app import db
from app.models.Guest import Guest
from app.models.Catalogs import Catalogs

class Item(db.Model):
    """Stores Item info"""
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    created_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(300))
    catalog_id = db.Column(db.Integer, db.ForeignKey('catalogs.id'))
    catalogs = db.relationship(Catalogs)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'))
    guest = db.relationship(Guest)

    @property
    def serialize(self):
        """Return Item object data in easily serializable format"""
        return {
            'id': self.id,
            'create_time': self.created_time,
            'name': self.name,
            'description': self.description
        }