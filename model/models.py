import uuid
from app import db

class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=str(uuid.uuid4()))
    # str conversion for mysql
    name = db.Column('name',db.String(100), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, phone_number={self.phone_number}, email={self.email})"

# db.create_all()