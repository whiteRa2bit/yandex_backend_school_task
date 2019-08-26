from app import db

class Citizen(db.Model):
	__tablename__ = 'people1'

	id = db.Column(db.Integer(), primary_key=True)
	citizen_id = db.Column(db.Integer())
	import_id = db.Column(db.Integer())
	town = db.Column(db.String()) ### string
	street = db.Column(db.String()) ### string
	building = db.Column(db.String()) ### string
	apartment =  db.Column(db.Integer())###int
	name = db.Column(db.String())### string
	birth_date = db.Column(db.String())### string dd.mm.yyyy
	gender = db.Column(db.String())### string
	relatives = db.Column(db.String())###list of int

	def __init__(self, citizen_id, import_id, town, street, building, apartment, name,\
					birth_date, gender, relatives):
		self.citizen_id = citizen_id
		self.import_id = import_id
		self.town = town
		self.street = street
		self.building = building
		self.apartment = apartment
		self.name = name
		self.birth_date = birth_date
		self.gender = gender
		self.relatives = relatives

	def __repr__(self):
		return '<id {}>'.format(self.id)


	def serialize(self):
		return {\
			# 'id': self.id,\
    		'citizen_id': self.citizen_id,\
    		# 'import_id': self.import_id,\
    		'town': self.town,\
    		'street': self.street,\
    		'building': self.building,\
    		'apartment': self.apartment,\
    		'name': self.name,\
    		'birth_date': self.birth_date,\
    		'gender': self.gender,\
    		'relatives': list(map(int, self.relatives.split()))\
    	}
