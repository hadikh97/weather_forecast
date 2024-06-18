import requests
from django.shortcuts import render
from datetime import datetime, timedelta

API_KEY = 'c53bb4104eb941a6b49144006241806'
API_URL = 'https://api.weatherapi.com/v1'


def get_weather_data(country):
    today = datetime.today()
    dates = {
        'yesterday': (today - timedelta(days=1)),
        'today': today,
        'tomorrow': (today + timedelta(days=1))
    }
    weather_data = {}
    for day, date in dates.items():
        response = requests.get(f'{API_URL}/forecast.json?key={API_KEY}&q={country}&dt={date.strftime("%Y-%m-%d")}')
        if response.status_code == 200:
            data = response.json()
            forecast = data.get('forecast', {}).get('forecastday', [])[0]
            weather_data[day] = {
                'day': date.strftime('%A'),  # Day of the week
                'condition': forecast.get('day', {}).get('condition', {}).get('text', ''),
                'icon': forecast.get('day', {}).get('condition', {}).get('icon', ''),
                'min_temp': forecast.get('day', {}).get('mintemp_c', ''),
                'max_temp': forecast.get('day', {}).get('maxtemp_c', '')
            }
        else:
            weather_data[day] = {
                'error': response.json().get('error', {}).get('message', 'Unknown error')
            }
    return weather_data


def weather_view(request):
    country = request.GET.get('country', 'USA')  # Default to USA if no country is specified
    weather_data = get_weather_data(country)
    return render(request, 'forecast/weather.html', {'weather_data': weather_data, 'country': country})
