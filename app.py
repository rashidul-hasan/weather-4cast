from flask import Flask, render_template, request, make_response
from flask.ext.bootstrap import Bootstrap
import json
from urllib.request import urlopen
from datetime import datetime, timedelta

app = Flask(__name__)
bootstrap = Bootstrap(app)

#get weather data from API
def get_weather(city):
    url = "http://api.openweathermap.org/data/2.5/forecast/daily?q={}&units=metric&cnt=7&mode=json&appid=70a40100d08b94013c81b36c30d5edc6".format(city.replace(' ', ''))
    response = urlopen(url).read().decode('utf8')
    return response

@app.route('/')
def index():
    search_city = request.args.get('searchcity')
    if not search_city:
        search_city = request.cookies.get('last_city')
    if not search_city:
        search_city = "Dhaka"

    forecast = []
    data = json.loads(get_weather(search_city))
    try:
        city = data['city']['name']
    except KeyError:
        return render_template('error.html', user_input=search_city)

    country = data.get('city').get('country')
    for item in data.get('list'):
        day = datetime.fromtimestamp(int(item.get('dt'))).strftime('%d %B, %Y')
        mini = item.get('temp').get('min')
        maxi = item.get('temp').get('max')
        description = item.get('weather')[0].get('description')
        icon = item.get('weather')[0].get('icon')
        forecast.append((day, mini, maxi, description, icon))
    response = make_response(render_template('index.html', data=forecast, city=city, country=country))
    response.set_cookie('last_city', '{}'.format(city), expires=datetime.today() + timedelta(hours=2))
    return response


if __name__ == "__main__":
    app.run(debug=True, port=8000)
