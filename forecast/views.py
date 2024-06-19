import requests
from django.conf import settings
from django.shortcuts import render
from datetime import datetime, timedelta
from .models import Weather

API_KEY = 'fc20461f33ae4e958b812325241906'
API_URL = 'https://api.weatherapi.com/v1'


def fetch_weather_data(country, date):
    response = requests.get(f'{API_URL}/forecast.json?key={API_KEY}&q={country}&dt={date.strftime("%Y-%m-%d")}')
    if response.status_code == 200:
        data = response.json()
        forecast = data.get('forecast', {}).get('forecastday', [])[0]
        return {
            'day': date.strftime('%A'),
            'condition': forecast.get('day', {}).get('condition', {}).get('text', ''),
            'icon': forecast.get('day', {}).get('condition', {}).get('icon', ''),
            'min_temp': forecast.get('day', {}).get('mintemp_c', ''),
            'max_temp': forecast.get('day', {}).get('maxtemp_c', '')
        }
    else:
        return None


def get_weather_data(country):
    today = datetime.today().date()
    dates = {
        'yesterday': today - timedelta(days=1),
        'today': today,
        'tomorrow': today + timedelta(days=1)
    }
    weather_data = {}

    for day, date in dates.items():
        weather = Weather.objects.filter(country=country, date=date).first()

        if not weather:
            data = fetch_weather_data(country, date)
            if data:
                weather = Weather(
                    country=country,
                    date=date,
                    day=data['day'],
                    condition=data['condition'],
                    icon=data['icon'],
                    min_temp=data['min_temp'],
                    max_temp=data['max_temp']
                )
                weather.save()
        if weather:
            weather_data[day] = {
                'day': weather.day,
                'condition': weather.condition,
                'icon': weather.icon,
                'min_temp': weather.min_temp,
                'max_temp': weather.max_temp
            }
        else:
            weather_data[day] = {
                'error': 'Unable to fetch weather data'
            }
    return weather_data


def weather_view(request):
    country = request.GET.get('country', 'USA')  # Default to USA if no country is specified
    weather_data = get_weather_data(country)
    return render(request, 'forecast/weather.html', {'weather_data': weather_data, 'country': country})
