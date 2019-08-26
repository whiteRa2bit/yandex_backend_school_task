import json
import requests
from urllib.parse import urlencode

def task1(url):
	citizens_data = []

	citizen1 = {
				"citizen_id": 3,\
				"town": '1-',\
				"street": "Льва Толстого",\
				"building": "1....",\
				"apartment": 9,\
				"name":	"Павел Александрович Факанов",\
				"birth_date": "01.04.2010",\
				"gender": "male",\
				"relatives": [2, 1, 10, 9]
				}
	citizens_data.append(citizen1)

	test_data = {"citizens": citizens_data}
	r = requests.post(url, json=test_data)
	print(r)
	print(r.text)
	print(r.status_code)

def task2(url):
	citizen = {
				"town": 'hello',\
				"apartment": 1,\
				"name":	"Pavel Fakanov",\
				"birth_date": "01.04.2001",\
				"gender": "e_female",\
				"relatives": [2]
				}
	r = requests.patch(url, json=citizen)
	print(r)
	print(r.text)
	print(r.status_code)

def task3(url):
	r = requests.get(url)
	print(r)
	print(r.text)
	print(r.status_code)

task1('http://0.0.0.0:8080/imports')
# task2('http://0.0.0.0:8080/imports/1/citizens/2')
# task3('http://0.0.0.0:8080/imports/1/citizens')