from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.weather'

db = SQLAlchemy(app)

class Weather(db.Model):
    id = db.Column(db.Integer(),primary_key = True)
    location = db.Column(db.String(50), nullable=False)

@app.route('/', methods = ['GET','POST'])
def weather_app(): 
    
    if request.method == 'POST' and 'city' in request.form:   
        city_input = request.form.get('city')
        new_city = Weather(location = city_input)
        db.session.add(new_city)
        db.session.commit()
    cities_in_db = Weather.query.all()
    city_details_list = []
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=157e46472c9f21dcd1bc7e70bc0f02a2'
    for i in cities_in_db:
        response = requests.get(url.format(i.location)).json()
        weather_data = {
            "location" : i.location,
            "temperature" : response['main']['temp'],
            "status" : response['weather'][0]['description'],
            "icon" :response['weather'][0]['icon']
            }
        city_details_list.append(weather_data)
    return render_template("weather.html",weather_data = weather_data)
if __name__ == '__main__':
    app.run()
