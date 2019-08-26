from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import os
import json
import urllib.parse
from flask import abort
from marshmallow import Schema, fields, validates, ValidationError, validates_schema
from marshmallow.validate import Length, Range
from datetime import datetime
from sqlalchemy import and_
import uuid
import random


class AddCitizensShema(Schema):
    citizen_id = fields.Int(required=True, validate=Range(min=0))
    town = fields.Str(required=True, validate=Length(min=1, max=256))
    street = fields.Str(required=True, validate=Length(min=1, max=256))
    building = fields.Str(required=True, validate=Length(min=1, max=256))
    apartment = fields.Int(required=True, validate=Range(min=0))
    name = fields.Str(required=True, validate=Length(min=1, max=256))
    birth_date = fields.Str(required=True)
    gender = fields.Str(required=True)
    relatives = fields.List(fields.Int, required=True)

    @validates_schema
    def is_appropriate_str_format_town(self, data, **kwargs):
        value = data['town']
        letters_num = len([c for c in value if c.isalpha()])
        digits_num = len([c for c in value if c.isdigit()])
        if letters_num + digits_num < 1:
           raise ValidationError("error str validation")

    @validates_schema
    def is_appropriate_str_format_street(self, data, **kwargs):
        value = data['street']
        letters_num = len([c for c in value if c.isalpha()])
        digits_num = len([c for c in value if c.isdigit()])
        if letters_num + digits_num < 1:
            raise ValidationError("error str validation")

    @validates_schema
    def is_appropriate_str_format_building(self, data, **kwargs):
        value = data['building']
        letters_num = len([c for c in value if c.isalpha()])
        digits_num = len([c for c in value if c.isdigit()])
        if letters_num + digits_num < 1:
            raise ValidationError("error str validation")
            

    @validates_schema
    def is_appropriate_gender(self, data, **kwargs):
        value = data['gender']
        if value not in ['male', 'female']:
            raise ValidationError("Can create citizens only with gender 'male' or 'female'")

    @validates_schema
    def is_valid_date(self, data, **kwargs):
        value = data['birth_date'] 
        try:
            datetime.strptime(value, '%d.%m.%Y')
        except:
            raise ValidationError("wrong date format")

        now = datetime.now()
        value_dt = datetime.strptime(value, '%d.%m.%Y')
        if value_dt > now:
            raise ValidationError("Can't create citizens with birth_date in the future!")


class ModifyCitizenInfoShema(Schema):
    town = fields.Str(required=False, validate=Length(min=1, max=256))
    street = fields.Str(required=False, validate=Length(min=1, max=256))
    building = fields.Str(required=False, validate=Length(min=1, max=256))
    apartment = fields.Int(required=False, validate=Range(min=0))
    name = fields.Str(required=False, validate=Length(min=1, max=256))
    birth_date = fields.Str(required=False)
    gender = fields.Str(required=False)
    relatives = fields.List(fields.Int, required=False)

    @validates_schema
    def is_appropriate_str_format_town(self, data, **kwargs):
        value = data['town']
        letters_num = len([c for c in value if c.isalpha()])
        digits_num = len([c for c in value if c.isdigit()])
        if letters_num + digits_num < 1:
           raise ValidationError("error str validation")

    @validates_schema
    def is_appropriate_str_format_street(self, data, **kwargs):
        value = data['street']
        letters_num = len([c for c in value if c.isalpha()])
        digits_num = len([c for c in value if c.isdigit()])
        if letters_num + digits_num < 1:
            raise ValidationError("error str validation")

    @validates_schema
    def is_appropriate_str_format_building(self, data, **kwargs):
        value = data['building']
        letters_num = len([c for c in value if c.isalpha()])
        digits_num = len([c for c in value if c.isdigit()])
        if letters_num + digits_num < 1:
            raise ValidationError("error str validation")
            

    @validates_schema
    def is_appropriate_gender(self, data, **kwargs):
        value = data['gender']
        if value not in ['male', 'female']:
            raise ValidationError("Can create citizens only with gender 'male' or 'female'")

    @validates_schema
    def is_valid_date(self, data, **kwargs):
        value = data['birth_date'] 
        try:
            datetime.strptime(value, '%d.%m.%Y')
        except:
            raise ValidationError("wrong date format")

        now = datetime.now()
        value_dt = datetime.strptime(value, '%d.%m.%Y')
        if value_dt > now:
            raise ValidationError("Can't create citizens with birth_date in the future!")

add_citizens_schema = AddCitizensShema()
modify_citizen_info_shema = ModifyCitizenInfoShema()

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Citizen

def get_import_id():
    COEF = 10000
    return (uuid.uuid1().int>>120) * COEF + random.sample(range(COEF), 1)[0]

@app.route("/imports", methods=['POST'])
def add_citizens():
	try:
		citizens_data = request.get_json()
		for i in range(len(citizens_data['citizens'])):
			errors = add_citizens_schema.validate(citizens_data['citizens'][i])
			if errors:
				return 'invalid', 400

		citizens_ids = []

		import_id = get_import_id()
		for chunk in range(0, len(citizens_data['citizens']), 5000):
			db.session.bulk_insert_mappings(
	            Citizen,\
	            [
	                dict(citizen_id = citizens_data['citizens'][i]['citizen_id'],\
						import_id = import_id,\
						town = citizens_data['citizens'][i]['town'],\
						street = citizens_data['citizens'][i]['street'],\
						building = citizens_data['citizens'][i]['building'],\
						apartment = citizens_data['citizens'][i]['apartment'],\
						name = citizens_data['citizens'][i]['name'],\
						birth_date = citizens_data['citizens'][i]['birth_date'],\
						gender = citizens_data['citizens'][i]['gender'],\
						relatives = ' '.join(list(map(str, citizens_data['citizens'][i]['relatives'])))
						)
	                for i in range(chunk, min(chunk + 5000, len(citizens_data['citizens'])))
	            ]
	        )
			db.session.commit()
		return jsonify({"data": {"import_id": import_id}}), 201

	except:
		abort(400) 



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

def upgrade_relatives_info(citizen_id, import_id, relatives):
	query = db.session.query(Citizen).filter(Citizen.import_id==import_id)
	rows = query.all()
	for row in rows:
		if row.citizen_id == citizen_id:
			continue

		if str(citizen_id) in row.relatives.split() and row.citizen_id not in relatives:
			row_relatives_list = row.relatives.split()
			row_relatives_list.remove(str(citizen_id))
			row.relatives = ' '.join(row_relatives_list)

		elif str(citizen_id) not in row.relatives.split() and row.citizen_id in relatives:
			row.relatives += ' ' + str(citizen_id)



@app.route('/imports/<import_id>/citizens/<citizen_id>', methods=['PATCH'])
def modify_citizens_info(import_id, citizen_id):
	try:
		new_citizen_data = request.get_json()
		errors = modify_citizen_info_shema.validate(new_citizen_data)
		if errors or not new_citizen_data:
			return str("invalid data"), 400

		citizen = db.session.query(Citizen).filter_by(citizen_id=citizen_id, import_id=import_id).first()

		upgrade_relatives_info(citizen_id, import_id, new_citizen_data['relatives'])
		for field in new_citizen_data.keys():
			citizen = modify_object(citizen, field, new_citizen_data[field])
		db.session.commit()

		return jsonify(citizen.serialize()), 200
	except Exception as e:
		return str("invalid data"), 400


@app.route('/imports/<import_id>/citizens', methods=['GET'])
def return_citizens_data(import_id):
	try:
		query = db.session.query(Citizen).filter(Citizen.import_id==import_id)
		rows = query.all()
		citizens_data = []

		for row in rows:
			citizens_data.append(row.serialize())
			# return str(type(row))
		# return str(len(rows))
		return jsonify({'data': citizens_data}), 200
		# return json.dumps({'data': citizens_data}, ensure_ascii=False), 200
	except:
		return str("invalid data"), 400


@app.route('/imports/<import_id>/citizens/birthdays', methods=['GET'])
def return_citizens_birthdays(import_id):
	try:
		query = db.session.query(Citizen).filter(Citizen.import_id==import_id)
		rows = query.all()
		# citizens_data = []

		birthdays = {i: {} for i in range(1, 13)}

		for row in rows:
			row_dt = datetime.strptime(row.birth_date, '%d.%m.%Y')
			for relative_id in list(map(int, row.relatives.split())):
				try:
					birthdays[row_dt.month][relative_id] += 1
				except KeyError:
					birthdays[row_dt.month][relative_id] = 1

		birthdays_to_return = {"data": {i: [] for i in range(1, 13)}}

		for month, users_dict in birthdays.items():
			for citizen_id, presents_num in users_dict.items():
				birthdays_to_return["data"][month].append({"citizen_id": citizen_id, "presents": presents_num})

		return jsonify(birthdays_to_return), 200
	except:
		abort(400)




app.run(host= '0.0.0.0', port=8080, debug=True)