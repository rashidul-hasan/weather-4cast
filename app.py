from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
import json
from urllib.request import urlopen
import time

app = Flask(__name__)
bootstrap = Bootstrap(app)

#get weather data from API
def get_weather():
    url = "http://api.openweathermap.org/data/2.5/forecast/daily?lat=35&lon=139&cnt=10&mode=json&appid=70a40100d08b94013c81b36c30d5edc6"
    response = urlopen(url).read()
    return response

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, port=8000)
