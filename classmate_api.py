
import requests

url = "https://jaya-mekaela-almodiel.onrender.com/student"

try:
    response = requests.get(url, timeout=30)
    print("Status Code:", response.status_code)

    if response.status_code == 200:
        data = response.json()
        print("Classmate's API Data:")
        print(data)
    else:
        print("Request failed.")
        print(response.text)

except requests.exceptions.RequestException as error:
    print("Connection error:", error)
