#!/usr/bin/env python3

from models import db, Sweet, Vendor, VendorSweet
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource, reqparse
import os

from models import db, Vendor, VendorSweet, Sweet

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('price', type=int, required=True, help='Price is required')
parser.add_argument('vendor_id', type=int, required=True, help='Vendor ID is required')
parser.add_argument('sweet_id', type=int, required=True, help='Sweet ID is required')

@app.route('/')
def home():
    return '<h1>Code challenge</h1>'

class VendorsResource(Resource):
    def get(self):
        vendors = Vendor.query.all()
        response = [vendor.to_dict() for vendor in vendors]
        return response
api.add_resource(VendorsResource, '/vendors')

class VendorsByIdResource(Resource):
    def get(self, vendor_id):
        vendor = Vendor.query.get(vendor_id)
        if vendor is None:
            return {"error": "Vendor not found"}, 404
        return vendor.to_dict()
api.add_resource(VendorsByIdResource, '/vendors/<int:vendor_id>')

class SweetsResource(Resource):
    def get(self):
        sweets = Sweet.query.all()
        response = [sweet.to_dict() for sweet in sweets]
        return response
api.add_resource(SweetsResource, '/sweets')

class SweetsByIdResource(Resource):
    def get(self, sweet_id):
        sweet = Sweet.query.get(sweet_id)
        if sweet is None:
            return {"error": "Sweet not found"}, 404
        return sweet.to_dict()
api.add_resource(SweetsByIdResource, '/sweets/<int:sweet_id>')

class VendorSweetsResource(Resource):
    def post(self):
        args = parser.parse_args()

        session = db.session

        vendor = session.get(Vendor, args['vendor_id'])
        sweet = session.get(Sweet, args['sweet_id'])

        if vendor is None or sweet is None:
            return {'error': 'Invalid vendor_id or sweet_id'}, 400

        vendor_sweet = VendorSweet(
            vendor_id=args['vendor_id'],
            sweet_id=args['sweet_id'],
            price=args['price']
        )

        session.add(vendor_sweet)
        session.commit()

        response = {
            'id': vendor_sweet.id,
            'name': sweet.name,  
            'price': vendor_sweet.price
        }
        return response, 201
api.add_resource(VendorSweetsResource, '/vendor_sweets')

class VendorSweetResource(Resource):
    def delete(self, vendor_sweet_id):
        vendor_sweet = VendorSweet.query.get(vendor_sweet_id)

        session = db.session
        if vendor_sweet:
            session.delete(vendor_sweet)
            session.commit()
            return {"message": f"VendorSweet with ID {vendor_sweet_id} successfully deleted"}, 200 
        else:
            return {"error": "VendorSweet not found"}, 404  

api.add_resource(VendorSweetResource, '/vendor_sweets/<int:vendor_sweet_id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
