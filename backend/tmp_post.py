import json
import urllib.request

data = {
    'flight_number': 'TS102',
    'origin': 'JFK',
    'destination': 'SEA',
    'departure_time': '2026-05-11T12:00:00',
    'arrival_time': '2026-05-11T16:00:00'
}

req = urllib.request.Request('http://127.0.0.1:5000/api/flights/', data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'}, method='POST')
try:
    with urllib.request.urlopen(req, timeout=5) as resp:
        print(resp.status, resp.read().decode())
except Exception as e:
    print('Error:', e)
