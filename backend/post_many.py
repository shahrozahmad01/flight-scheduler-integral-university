"""Post multiple unique flights to the running backend for final smoke test."""
import json
import time
import urllib.request

BASE = 'http://127.0.0.1:5000'

def post_flight(flight):
    url = BASE + '/api/flights/'
    data = json.dumps(flight).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status, json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode('utf-8')
            return e.code, json.loads(body)
        except Exception:
            return e.code, {'error': str(e)}
    except Exception as e:
        return None, {'error': str(e)}

def main():
    results = []
    for i in range(200, 210):
        flight = {
            'flight_number': f'TS{i}',
            'origin': 'JFK',
            'destination': 'LAX' if i % 2 == 0 else 'SFO',
            'departure_time': '2026-05-12T08:00:00',
            'arrival_time': '2026-05-12T12:00:00'
        }
        status, body = post_flight(flight)
        print(f'POST {flight["flight_number"]}:', status, body)
        results.append((flight['flight_number'], status, body))
        time.sleep(0.2)

    print('\nListing flights summary...')
    try:
        with urllib.request.urlopen(BASE + '/api/flights/', timeout=5) as resp:
            all_flights = json.loads(resp.read().decode('utf-8'))
            print('Total flights returned:', len(all_flights))
    except Exception as e:
        print('Error listing flights:', e)

if __name__ == '__main__':
    main()
