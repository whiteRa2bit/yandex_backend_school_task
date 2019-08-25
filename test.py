import json
import requests
from urllib.parse import urlencode


url = 'http://0.0.0.0:8080/imports'


citizens_data = []

citizen1 = {
			"citizen_id": 3,\
			"town": "Москва",\
			"street": "Льва Толстого",\
			"building": "16к7стр2",\
			"apartment": 7,\
			"name":	"Павел Александрович Факанов",\
			"birth_date": "26.12.1986",\
			"gender": "male",\
			"relatives": [2]
			}
citizens_data.append(citizen1)


test_data = {"citizens": citizens_data}
r = requests.post(url, json=test_data)
print(r)
print(r.text)
print(r.status_code)