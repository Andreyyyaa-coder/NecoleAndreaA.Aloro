
import requests

PARTNER_API_URL = (
    "https://balcenajessicaann-2axr.onrender.com/api/students"
)

record = {
    "student_id": "EXT-001",
    "name": "Sample Exchange Record",
    "program": "BSIT",
    "year": 1,
    "section": "A",
    "source": "Partner API"
}

try:
    response = requests.post(
        PARTNER_API_URL,
        json=record,
        timeout=30
    )

    print("Status Code:", response.status_code)
    print("Response:")

    try:
        print(response.json())
    except ValueError:
        print(response.text)

except requests.RequestException as error:
    print("Request failed:", error)
