from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import os
import json
import urllib.parse
from flask import abort
from marshmallow import Schema, fields, validates, ValidationError
from datetime import datetime

class CreateNoteInputSchema(Schema):
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
            raise ValidationError("Can't create notes in the future!")

create_note_schema = CreateNoteInputSchema()


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Citizen


@app.route("/imports", methods=['POST'])
def add_citizens():

	citizens_data = request.get_json()
	errors = create_note_schema.validate(citizens_data['citizens'][0])
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


app.run(host= '0.0.0.0', port=8080, debug=True)