import requests

url = "http://127.0.0.1:8001/auth/register"
data = {
    "username": "admin",
    "password": "admin123",
    "full_name": "admin"
}
headers = {"Content-Type": "application/json"}
response = requests.post(url, json=data, headers=headers)
print(response.status_code)
print(response.json())