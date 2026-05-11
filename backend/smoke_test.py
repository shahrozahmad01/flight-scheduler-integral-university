"""Simple smoke test script for backend API.

Usage: python backend/smoke_test.py
"""
import json
import urllib.request
import urllib.error

BASE = 'http://127.0.0.1:5000'

def req(path, method='GET', data=None):
    url = BASE + path
    headers = {'Content-Type': 'application/json'}
    data_bytes = None
    if data is not None:
        data_bytes = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(url, data=data_bytes, headers=headers, method=method)
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
    print('Checking root endpoint...')
    status, body = req('/')
    print(status, body)

    print('Listing flights (should be empty or list)...')
    status, body = req('/api/flights/')
    print(status, body)

    print('Creating a sample flight...')
    flight = {
        'flight_number': 'TS100',
        'origin': 'JFK',
        'destination': 'LAX',
        'departure_time': '2026-05-11T10:00:00',
        'arrival_time': '2026-05-11T14:00:00'
    }
    status, body = req('/api/flights/', method='POST', data=flight)
    print('POST /api/flights/', status, body)

    print('Listing flights again...')
    status, body = req('/api/flights/')
    print(status, body)

if __name__ == '__main__':
    main()
