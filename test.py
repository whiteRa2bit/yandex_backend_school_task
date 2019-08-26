import json
import requests
from urllib.parse import urlencode

def task1(url):
	citizens_data = []

	citizen1 = {
				"citizen_id": 1,\
				"town": '...1',\
				"street": "@@@2	",\
				"building": "12",\
				"apartment": 1,\
				"name":	"Artem",\
				"birth_date": "01.04.2000",\
				"gender": "male",\
				"relatives": [2, 3]
				}
	citizen2 = {
				"citizen_id": 2,\
				"town": '1',\
				"street": "Литовский",\
				"building": "1",\
				"apartment": 120,\
				"name":	"Fakanov Pavel",\
				"birth_date": "01.04.1999",\
				"gender": "male",\
				"relatives": [1]
				}
	citizen3 = {
				"citizen_id": 3,\
				"town": '///1',\
				"street": "Бабушкинская",\
				"building": "...1",\
				"apartment": 10,\
				"name":	"Kirill",\
				"birth_date": "11.10.1998",\
				"gender": "male",\
				"relatives": [1]
				}

	citizens_data.append(citizen1)
	citizens_data.append(citizen2)
	citizens_data.append(citizen3)

	test_data = {"citizens": citizens_data}
	r = requests.post(url, json=test_data)
	print(r)
	print(r.text)
	print(r.status_code)

def task2(url):
	citizen = {
				# "town": 'Можайск',\
				# "apartment": 10,\
				# "name":	"Женя Факанов",\
				# "birth_date": "01.04.1901",\
				# "gender": "male",\
				# "relatives": [1, 2]
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

def task4(url):
	r = requests.get(url)
	print(r)
	print(r.text)
	print(r.status_code)


task1('http://0.0.0.0:8080/imports')
# task2('http://0.0.0.0:8080/imports/2550030/citizens/3')
# task3('http://0.0.0.0:8080/imports/1149160/citizens')
# task4('http://0.0.0.0:8080/imports/1149160/citizens/birthdays')
