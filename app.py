from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import os
import json
import urllib.parse
from flask import abort
from marshmallow import Schema, fields, validates, ValidationError
from datetime import datetime
from sqlalchemy import and_

class AddCitizensShema(Schema):
    citizen_id = fields.Int(required=True)
    town = fields.Str(required=True)
    street = fields.Str(required=True)
    building = fields.Str(required=True)
    apartment = fields.Int(required=True)
    name = fields.Str(required=True)
    birth_date = fields.Str(required=True)
    gender = fields.Str(required=True)
    relatives = fields.List(fields.Int, required=True)

    @validates('birth_date')
    def is_not_in_future(self, value):	
        """'value' is the datetime parsed from time_created by marshmallow"""
        now = datetime.now()
        value_dt = datetime.strptime(value, '%d.%m.%Y')
        if value_dt > now:
            raise ValidationError("Can't create citizens with birth_date in the future!")


class ModifyCitizenInfoShema(Schema):
    town = fields.Str(required=False)
    street = fields.Str(required=False)
    building = fields.Str(required=False)
    apartment = fields.Int(required=False)
    name = fields.Str(required=False)
    birth_date = fields.Str(required=False)
    gender = fields.Str(required=False)
    relatives = fields.List(fields.Int, required=True)

add_citizens_schema = AddCitizensShema()
modify_citizen_info_shema = ModifyCitizenInfoShema()

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Citizen


@app.route("/imports", methods=['POST'])
def add_citizens():

	citizens_data = request.get_json()
	errors = add_citizens_schema.validate(citizens_data['citizens'][0])
	if errors:
		abort(400)

	citizens_ids = []

	import_id = 1
	for data in citizens_data['citizens']:
		try:
			citizen = Citizen(
					citizen_id = data['citizen_id'],\
					import_id = import_id,\
					town = data['town'],\
					street = data['street'],\
					building = data['building'],\
					apartment = data['apartment'],\
					name = data['name'],\
					birth_date = data['birth_date'],\
					gender = data['gender'],\
					relatives = ' '.join(list(map(str, data['relatives'])))
				)
			db.session.add(citizen)
			db.session.commit()
			citizens_ids.append(citizen.citizen_id)


		except Exception as e:  ### CHANGE IT LATER!!!!!!!!!!!!!
			abort(400) 
	return jsonify({"data": {"import_id": import_id}}), 201



def modify_object(citizen, field, value):
	if field == 'town':
		citizen.town = value
	if field == 'street':
		citizen.street = value
	if field == 'building':
		citizen.building = value
	if field == 'apartment':
		citizen.apartment = value
	if field == 'name':
		citizen.name = value
	if field == 'birth_date':
		citizen.birth_date = value
	if field == 'gender':
		citizen.gender = value
	if field == 'relatives':
		citizen.relatives = ' '.join(list(map(str, value)))
	return citizen

@app.route('/imports/<import_id>/citizens/<citizen_id>', methods=['PATCH'])
def modify_citizens_info(import_id, citizen_id):
	new_citizen_data = request.get_json()
	# errors = modify_citizen_info_shema.validate(new_citizen_data)
	# if errors:
	# 	abort(400)

	citizen = db.session.query(Citizen).filter_by(citizen_id=citizen_id, import_id=import_id).first()

	for field in new_citizen_data.keys():
		citizen = modify_object(citizen, field, new_citizen_data[field])
		# citizen.name = 'Fakanov'

	db.session.commit()

	# return str(citizen.serialize()['name'])
	return jsonify(citizen.serialize()), 200


@app.route('/imports/<import_id>/citizens', methods=['GET'])
def return_citizens_data(import_id):
	query = db.session.query(Citizen).filter(Citizen.import_id==import_id)
	rows = query.all()
	citizens_data = []

	for row in rows:
		citizens_data.append(row.serialize())
		# return str(type(row))
	# return str(len(rows))
	return jsonify({'data': citizens_data}), 200



app.run(host= '0.0.0.0', port=8080, debug=True)