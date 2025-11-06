"""
Weather Service
Fetches weather forecast data from OpenWeatherMap API
For dates beyond 5 days, uses Open-Meteo climate data
"""
import requests
from datetime import datetime, timedelta
from config import Config
import logging
import urllib3
import calendar

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)

class WeatherService:
    """Service for fetching weather data"""
    
    def __init__(self):
        self.api_key = Config.OPENWEATHER_API_KEY
        self.base_url = Config.OPENWEATHER_BASE_URL
    
    def get_weather_forecast(self, destination, start_date, end_date):
        """
        Get weather forecast for destination and date range

        Args:
            destination: City name (e.g., "Paris, France")
            start_date: Start date string (YYYY-MM-DD)
            end_date: End date string (YYYY-MM-DD)

        Returns:
            Dictionary with weather forecast data
        """
        try:
            # First, get coordinates for the destination
            coords = self._get_coordinates(destination)

            if not coords:
                logger.warning(f"Could not find coordinates for {destination}")
                return None

            # Check if dates are within 5 days
            start = datetime.strptime(start_date, '%Y-%m-%d')
            days_until_trip = (start - datetime.now()).days

            if days_until_trip <= 5:
                # Use real forecast for near-term trips
                forecast = self._get_forecast(coords['lat'], coords['lon'], start_date, end_date)
                data_type = 'forecast'
            else:
                # Use climate data for future trips
                forecast = self._get_climate_data(coords['lat'], coords['lon'], start_date, end_date)
                data_type = 'climate'

            return {
                'destination': destination,
                'coordinates': coords,
                'forecast': forecast,
                'summary': self._generate_summary(forecast, data_type),
                'data_type': data_type
            }

        except Exception as e:
            logger.error(f"Error fetching weather data: {str(e)}")
            return None
    
    def _get_coordinates(self, destination):
        """Get lat/lon coordinates for a destination"""
        url = f"http://api.openweathermap.org/geo/1.0/direct"
        params = {
            'q': destination,
            'limit': 1,
            'appid': self.api_key
        }

        try:
            response = requests.get(url, params=params, timeout=10, verify=False)
            response.raise_for_status()
            
            data = response.json()
            
            if data:
                return {
                    'lat': data[0]['lat'],
                    'lon': data[0]['lon'],
                    'name': data[0].get('name', destination),
                    'country': data[0].get('country', ''),
                    'state': data[0].get('state', '')
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting coordinates: {str(e)}")
            return None
    
    def _get_forecast(self, lat, lon, start_date, end_date):
        """Get weather forecast for coordinates and date range"""
        url = f"{self.base_url}/forecast"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': 'metric'  # Celsius
        }

        try:
            response = requests.get(url, params=params, timeout=10, verify=False)
            response.raise_for_status()

            data = response.json()
            
            # Parse forecast data
            forecast = []
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')
            
            # Group by date
            daily_data = {}
            
            for item in data.get('list', []):
                dt = datetime.fromtimestamp(item['dt'])
                date_str = dt.strftime('%Y-%m-%d')
                
                # Only include dates in our range
                if start <= dt <= end + timedelta(days=1):
                    if date_str not in daily_data:
                        daily_data[date_str] = {
                            'temps': [],
                            'conditions': [],
                            'rain_chances': [],
                            'humidity': [],
                            'wind_speed': []
                        }
                    
                    daily_data[date_str]['temps'].append(item['main']['temp'])
                    daily_data[date_str]['conditions'].append(item['weather'][0]['description'])
                    daily_data[date_str]['rain_chances'].append(
                        item.get('pop', 0) * 100  # Probability of precipitation
                    )
                    daily_data[date_str]['humidity'].append(item['main']['humidity'])
                    daily_data[date_str]['wind_speed'].append(item['wind']['speed'])
            
            # Aggregate daily data
            for date_str, data in sorted(daily_data.items()):
                forecast.append({
                    'date': date_str,
                    'day': datetime.strptime(date_str, '%Y-%m-%d').strftime('%A'),
                    'temp_max': round(max(data['temps']), 1),
                    'temp_min': round(min(data['temps']), 1),
                    'temp_avg': round(sum(data['temps']) / len(data['temps']), 1),
                    'condition': max(set(data['conditions']), key=data['conditions'].count),
                    'rain_chance': round(max(data['rain_chances'])),
                    'humidity': round(sum(data['humidity']) / len(data['humidity'])),
                    'wind_speed': round(sum(data['wind_speed']) / len(data['wind_speed']), 1)
                })
            
            return forecast
            
        except Exception as e:
            logger.error(f"Error getting forecast: {str(e)}")
            return []

    def _get_climate_data(self, lat, lon, start_date, end_date):
        """Get typical climate data for the location and time of year"""
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')

            # Use Open-Meteo Climate API (free, no API key needed)
            url = "https://climate-api.open-meteo.com/v1/climate"
            params = {
                'latitude': lat,
                'longitude': lon,
                'start_date': start_date,
                'end_date': end_date,
                'daily': 'temperature_2m_mean,temperature_2m_max,temperature_2m_min,precipitation_sum',
                'temperature_unit': 'celsius'
            }

            response = requests.get(url, params=params, timeout=15, verify=False)
            response.raise_for_status()
            data = response.json()

            forecast = []
            daily = data.get('daily', {})

            if 'time' in daily:
                for i, date_str in enumerate(daily['time']):
                    temp_max = daily['temperature_2m_max'][i]
                    temp_min = daily['temperature_2m_min'][i]
                    temp_avg = daily['temperature_2m_mean'][i]
                    precip = daily['precipitation_sum'][i]

                    # Estimate condition based on precipitation
                    if precip > 5:
                        condition = "rainy"
                        rain_chance = 70
                    elif precip > 2:
                        condition = "partly cloudy with showers"
                        rain_chance = 50
                    elif precip > 0.5:
                        condition = "mostly cloudy"
                        rain_chance = 30
                    else:
                        condition = "mostly sunny"
                        rain_chance = 10

                    forecast.append({
                        'date': date_str,
                        'day': datetime.strptime(date_str, '%Y-%m-%d').strftime('%A'),
                        'temp_max': round(temp_max, 1),
                        'temp_min': round(temp_min, 1),
                        'temp_avg': round(temp_avg, 1),
                        'condition': condition,
                        'rain_chance': rain_chance,
                        'humidity': 65,  # Average estimate
                        'wind_speed': 3.5  # Average estimate
                    })

            return forecast

        except Exception as e:
            logger.error(f"Error getting climate data: {str(e)}")
            return []

    def _generate_summary(self, forecast, data_type='forecast'):
        """Generate a human-readable weather summary"""
        if not forecast:
            return "Weather forecast not available"

        temps = [day['temp_avg'] for day in forecast]
        rain_chances = [day['rain_chance'] for day in forecast]

        avg_temp = round(sum(temps) / len(temps), 1)
        max_temp = max(day['temp_max'] for day in forecast)
        min_temp = min(day['temp_min'] for day in forecast)
        avg_rain = round(sum(rain_chances) / len(rain_chances))

        # Add prefix based on data type
        if data_type == 'climate':
            prefix = "Typical weather for this time of year: "
        else:
            prefix = ""

        summary = f"{prefix}Average temperature: {avg_temp}°C (Range: {min_temp}°C to {max_temp}°C). "

        if avg_rain > 60:
            summary += "High chance of rain - pack an umbrella!"
        elif avg_rain > 30:
            summary += "Some rain possible - bring a light rain jacket."
        else:
            summary += "Mostly dry weather expected."

        return summary
