import urllib.request
import json

data = json.dumps({"transcript": "She built a tracking system and reduced delays by improving the process."}).encode("utf-8")
req = urllib.request.Request("http://localhost:5000/api/analyze", data=data, headers={"Content-Type": "application/json"})
resp = urllib.request.urlopen(req)
print(resp.status)
print(resp.read().decode())

