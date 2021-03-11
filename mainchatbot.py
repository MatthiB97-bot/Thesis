import requests
import json


url = "http://localhost:8080/engine-rest/decision-definition/key/Decision_056yjdp/evaluate"

input = {"variables" : {"ski_level" : { "value" : "Beginner", "type" : "string" },"ski_style" : {"value": "Slow", "type" : "string" }}}
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=json.dumps(input))

print(response.text)
