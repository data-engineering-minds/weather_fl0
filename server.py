import requests, os
from flask import Flask, render_template

app = Flask(__name__)

API_KEY = os.environ.get('API_KEY')
CITIES = {'berlin': 'Berlin,de', 'hamburg': 'Hamburg,de', 'dusseldorf': 'Dusseldorf,de',
          'munich': 'Munich,de', 'cologne': 'Cologne,de', 'frankfurt': 'Frankfurt,de',
          'stuttgart': 'Stuttgart,de', 'dresden': 'Dresden,de', 'nuremberg': 'Nuremberg,de',
          'leipzig': 'Leipzig,de', 'hannover': 'Hannover,de', 'bremen': 'Bremen,de',
          'bonn': 'Bonn,de', 'aachen': 'Aachen,de', 'freiburg': 'Freiburg,de',
          'kiel': 'Kiel,de', 'bielefeld': 'Bielefeld,de', 'erfurt': 'Erfurt,de',
          'rostock': 'Rostock,de', 'magdeburg': 'Magdeburg,de', 'wiesbaden': 'Wiesbaden,de',
          'kassel': 'Kassel,de', 'saarbrucken': 'Saarbrucken,de', 'potsdam': 'Potsdam,de',
          'wurzburg': 'Wurzburg,de', 'ulm': 'Ulm,de', 'mannheim': 'Mannheim,de'}


def get_weather_data(city):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    return response.json()

@app.route('/')
def get_weather_data_all_cities():
    weather_data = {}
    for city, city_name in CITIES.items():
        data = get_weather_data(city.lower())
        weather_data[city] = {
            'city_name': city,
            'temperature': data['main']['temp'],
            'weather_description': data['weather'][0]['description'],
            'feel_temperature': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure']
        }

    return render_template('weather.html', weather_data=weather_data)

if __name__ == '__main__':
     port = int(os.environ.get('PORT', 5000))
     app.run(host='0.0.0.0', port=port)