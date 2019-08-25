from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import os
import json
import urllib.parse

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Citizen

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/imports", methods=['POST'])
def add_citizens():
	# data = json.loads(request)
	# print(data)
	# print(request.args.get("citizens"))
	# return str(request.args.get("citizens"))
	# print(request.args.get("citizens")[0]['town'])
	# return '200'
	# citizens_data =  request.args.get('citizens')
	citizens_data = request.get_json()
	citizens_ids = []
	# return str((citizens_data['citizens']))

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
			# return str(type(data['relatives'][0]))

			db.session.add(citizen)

			db.session.commit()
			citizens_ids.append(citizen.citizen_id)


		except Exception as e:  ### CHANGE IT LATER!!!!!!!!!!!!!
			return(str(e)) 
	return jsonify({"data": {"import_id": import_id}}), 201


app.run(host= '0.0.0.0', port=8080, debug=True)