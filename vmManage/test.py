import json
import sys
import requests


url = "http://10.12.248.22:5000/ips/"
data = {
    "fixed_ip":{
      "subnet_id": "b0d39ab5-3f4c-4cd7-8195-56e0f1a81413"
		}
    }
headers = {
    "Content-Type": "application/json",
    # "Content-Length": str(sys.getsizeof(data)),
}

response = requests.post(url,headers=headers,data=json.dumps(data))
res = json.loads(response.text)
print(res['fixed_ips'][0]['ip_address'])