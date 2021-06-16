import requests
import json

url = "http://127.0.0.1:5000/user/login"

# payload = json.dumps({
#   "username": "steven2",
#   "email": "steven@steven.ste",
#   "password": "steven"
# })

payload = json.dumps({
  "username": "steven2",
  "password": "steven"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)
#print(payload)
print(response.text)