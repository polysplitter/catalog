from app import db
from app.models.Guest import Guest

class Catalogs(db.Model):
    """Stores Catalog info"""
    __tablename__ = 'catalogs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'))
    guest = db.relationship(Guest)

    @property
    def serialize(self):
        """Return Catalog object data in easily serializable format"""
        return {
            'id': self.id,
            'name': self.name
        }