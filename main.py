from flask import Flask, request, jsonify
import requests
from datetime import datetime
import os 

class WeatherAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'http://api.weatherapi.com/v1/history.json'

    def get_weather_data(self, location, date):
        response = requests.get(self.base_url, params={
            'key': self.api_key,
            'q': location,
            'dt': date 
        })
        response.raise_for_status()
        return response.json()

class GeminiAPI:
    def __init__(self, gemini_api_key):
        self.gemini_api_key = gemini_api_key
        self.url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent'

    def generate_article(self, attributes, style, language):
        headers = {'Content-Type': 'application/json'}
        prompt = (
            f"Create a {style} article with TITLE, PEREX and BODY about the weather based on the following attributes:\n"
            f"Language: {language}\n"
            f"Location: {attributes['location']}, Region: {attributes['region']}, Country: {attributes['country']}\n"
            f"Date: {attributes['forecast_date']}\n"
            f"Current Temperature: {attributes['temp_c']}°C\n"
            f"Condition: {attributes['condition']}\n"
            f"High Temperature: {attributes['high_temp']}°C, Low Temperature: {attributes['low_temp']}°C\n"
            f"Wind Speed: {attributes['wind_kph']} km/h\n"
            f"Humidity: {attributes['humidity']}%\n"
        )
        
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        
        response = requests.post(self.url, headers=headers, json=data, params={'key': self.gemini_api_key})
        response.raise_for_status()
        return response.json()

app = Flask(__name__)

weather_api_key = os.getenv('WEATHER_API_KEY')
gemini_api_key = os.getenv('GEMINI_API_KEY')

weather_api = WeatherAPI(weather_api_key)
gemini_api = GeminiAPI(gemini_api_key)

@app.route('/weather', methods=['GET'])
def get_weather():
    location = request.args.get('location')
    date = request.args.get('date')
    style = request.args.get('style', 'facts')
    language = request.args.get('language', 'en')

    if not location:
        return jsonify({'error': 'Location parameter is required.'}), 400

    if not date:
        return jsonify({'error': 'Date parameter is required.'}), 400

    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use "YYYY-MM-DD".'}), 400

    try:
        weather_data = weather_api.get_weather_data(location, date)

        if 'error' in weather_data:
            return jsonify({'error': weather_data['error']['message']}), 404

        attributes = {
            'location': weather_data['location']['name'],
            'region': weather_data['location']['region'],
            'country': weather_data['location']['country'],
            'temp_c': weather_data['forecast']['forecastday'][0]['day']['avgtemp_c'], 
            'condition': weather_data['forecast']['forecastday'][0]['day']['condition']['text'],
            'forecast_date': weather_data['forecast']['forecastday'][0]['date'],
            'high_temp': weather_data['forecast']['forecastday'][0]['day']['maxtemp_c'],
            'low_temp': weather_data['forecast']['forecastday'][0]['day']['mintemp_c'],
            'wind_kph': weather_data['forecast']['forecastday'][0]['day']['maxwind_kph'],
            'humidity': weather_data['forecast']['forecastday'][0]['day']['avghumidity'],
        }

        article_response = gemini_api.generate_article(attributes, style, language)
        article_text = article_response['candidates'][0]['content']['parts'][0]['text']

        return jsonify({'article': article_text})

    except requests.HTTPError as e:
        return jsonify({'error': f'{e.response.status_code} Client Error: {e.response.reason}'}), e.response.status_code
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
