import requests

response = requests.get('http://localhost:5000/rainfall-api/v1/years/2010/data')
response.json()



