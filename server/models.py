from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Vendor(db.Model, SerializerMixin):
    __tablename__ = 'vendors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    create_at=db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    update_at=db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Add relationship
    vendor_sweets = db.relationship('VendorSweet', back_populates='vendor')
    
    # Add serialization
    serialize_rules = ('-vendor_sweets.vendor',)
    
    def __repr__(self):
        return f'<Vendor {self.id}>'

class Sweet(db.Model, SerializerMixin):
    __tablename__ = 'sweets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Add relationship
    vendor_sweets = db.relationship('VendorSweet', back_populates='sweet')

    # Add serialization
    
    def __repr__(self):
        return f'<Sweet {self.id}>'



class VendorSweet(db.Model, SerializerMixin):
    __tablename__ = 'vendor_sweets'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)
    sweet_id = db.Column(db.Integer, db.ForeignKey('sweets.id'), nullable=False)
    
    # Add relationships
    vendor = db.relationship('Vendor', back_populates='vendor_sweets')
    sweet = db.relationship('Sweet', back_populates='vendor_sweets')

    # Add serialization
    serialize_rules = ('-vendor', '-sweet')
    
    # Add validation
    @db.validates('price')
    def validate_price(self, key, price):
        if not price:
            raise ValueError('Price cannot be blank')
        if price < 0:
            raise ValueError("Price can't be negative number")
        return price
    
    def __repr__(self):
        return f'<VendorSweet {self.id}>'
