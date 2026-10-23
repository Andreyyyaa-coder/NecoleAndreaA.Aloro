
import requests

url = "https://necoleandreaa-aloro.onrender.com/greet"

params = {
    "name": "Necole Andrea Aloro",
    "program": "BSIT",
    "year": 3,
    "section": "A"
}

response = requests.get(url, params=params)

print("Status Code:", response.status_code)

if response.status_code == 200:
    data = response.json()

    print("GREET ENDPOINT RESPONSE:")
    print(data)
else:
    print("Request failed.")
    print(response.text)
