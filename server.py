import requests, os, logging
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import date
from sqlalchemy import PrimaryKeyConstraint

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)

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

class ClickUrl(db.Model):
    url = db.Column(db.String(200), nullable=False)
    click_count = db.Column(db.Integer, nullable=False, default=0)
    click_date = db.Column(db.Date, nullable=False, default=date.today())

    __table_args__ = (
        PrimaryKeyConstraint('url', 'click_date', name ='_url_date_pk'),
    )

class CitySelection(db.Model):
    city = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False, default=date.today())
    select_count = db.Column(db.Integer, nullable=False, default=0)

    __table_args__ = (
        PrimaryKeyConstraint('city', 'date', name ='_city_date_pk'),
    )

def get_click_count(today):
    click_count_entry = ClickUrl.query.filter_by(url ='/', click_date=today).first()
    return 0 if click_count_entry is None else click_count_entry.click_count

def get_weather_data(city):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    response = requests.get(url)
    return response.json()

@app.route('/track_city_selection', methods=['POST'])
def track_city_selection():
    selected_city = request.form.get('selectedCity')

    if selected_city:
        today = date.today()
        city_selection = CitySelection.query.filter_by(city=selected_city, date=today).first()
        if city_selection is None:
            city_selection = CitySelection(city=selected_city, select_count=1, date=today)
            db.session.add(city_selection)
        else:
            city_selection.select_count += 1

        db.session.commit()
        return "City selection recorded successfully", 200
    else:
        return "Invalid city selection", 400

@app.route('/most_selected_city', methods=['GET'])
def get_most_selected_city():
    today = date.today()
    most_selected_city = CitySelection.query.order_by(CitySelection.select_count.desc()).filter_by(date=today).first()

    if most_selected_city:
        city_data = get_weather_data(most_selected_city.city.lower())
        return jsonify({
            'city_name': city_data['name'],
            'temperature': city_data['main']['temp'],
            'weather_description': city_data['weather'][0]['description'],
            'feel_temperature': city_data['main']['feels_like'],
            'humidity': city_data['main']['humidity'],
            'pressure': city_data['main']['pressure']
        })
    else:
        return jsonify({'message': 'No city selected yet'}), 404


@app.route('/')
def get_weather_data_all_cities():
    LOGGER.info('Getting weather data for all cities')
    today = date.today()

    click_count_entry = ClickUrl.query.filter_by(url='/', click_date=today).first()
    if click_count_entry is None:
        click_count_entry = ClickUrl(url='/', click_count=1, click_date=today)
        db.session.add(click_count_entry)
    else:
        click_count_entry.click_count += 1
    db.session.commit()
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

    click_count = get_click_count(today)

    return render_template('weather.html', weather_data=weather_data, click_count=click_count)

if __name__ == '__main__':
     port = int(os.environ.get('PORT', 5000))
     with app.app_context():
         db.create_all()
     app.run(host='0.0.0.0', port=port)