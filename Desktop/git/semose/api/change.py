import requests

def get_lat_lng_from_address(address, api_key="AIzaSyAGWaw80N-4bPYXLZjtep8SW6Gs5HxE1pA"):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": api_key,
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        lat = location['lat']
        lng = location['lng']
        return lat, lng
    else:
        return None
    
