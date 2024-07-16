import json

import requests

s = requests.Session()

# Connexion
payload = {
  "email": "gabrieltrouve5@gmail.com",
  "password": ""
}
headers = {'Content-type': 'application/json'}
r = s.post("http://127.0.0.1:8000/api/account/login", data=json.dumps(payload), headers=headers)

print(r.text)

# Vérification de l'état de connexion
r = s.get("http://127.0.0.1:8000/api/account/is_logged_in")

print(r.text)

