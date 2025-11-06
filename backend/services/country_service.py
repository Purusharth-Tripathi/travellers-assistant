"""
Country Service
Fetches country information from REST Countries API
"""
import requests
from config import Config
import logging
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)

class CountryService:
    """Service for fetching country information"""
    
    def __init__(self):
        self.base_url = Config.REST_COUNTRIES_BASE_URL
    
    def get_country_info(self, country_name):
        """
        Get country information

        Args:
            country_name: Name of the country

        Returns:
            Dictionary with country information
        """
        try:
            # Try to fetch country data
            url = f"{self.base_url}/name/{country_name}"
            response = requests.get(url, timeout=10, verify=False)
            response.raise_for_status()

            data = response.json()

            if data:
                country = data[0]  # Take first match
                return self._parse_country_data(country)

            return None

        except Exception as e:
            logger.error(f"Error fetching country info: {str(e)}")
            return None

    def get_country_info_by_code(self, country_code):
        """
        Get country information by 2-letter ISO country code

        Args:
            country_code: 2-letter ISO country code (e.g., 'FR', 'US', 'JP')

        Returns:
            Dictionary with country information
        """
        try:
            # Fetch country data by code
            url = f"{self.base_url}/alpha/{country_code}"
            response = requests.get(url, timeout=10, verify=False)
            response.raise_for_status()

            # The API returns a list with one country when searching by code
            data = response.json()

            # Check if it's a list or a single object
            if isinstance(data, list) and len(data) > 0:
                country = data[0]
            elif isinstance(data, dict):
                country = data
            else:
                return None

            return self._parse_country_data(country)

        except Exception as e:
            logger.error(f"Error fetching country info by code '{country_code}': {str(e)}")
            return None
    
    def _parse_country_data(self, country):
        """Parse country data from API response"""
        
        # Extract currency info
        currencies = country.get('currencies', {})
        currency_info = []
        for code, details in currencies.items():
            currency_info.append(f"{details.get('name')} ({code}) - {details.get('symbol', '')}")
        
        # Extract languages
        languages = list(country.get('languages', {}).values())
        
        # Extract timezone
        timezones = country.get('timezones', [])
        
        return {
            'name': country.get('name', {}).get('common', ''),
            'official_name': country.get('name', {}).get('official', ''),
            'capital': country.get('capital', [''])[0] if country.get('capital') else '',
            'region': country.get('region', ''),
            'subregion': country.get('subregion', ''),
            'population': country.get('population', 0),
            'area': country.get('area', 0),
            'currency': ', '.join(currency_info),
            'currencies_raw': currencies,
            'languages': languages,
            'timezone': timezones[0] if timezones else '',
            'timezones_all': timezones,
            'calling_code': country.get('idd', {}).get('root', '') + 
                           (country.get('idd', {}).get('suffixes', [''])[0] if country.get('idd', {}).get('suffixes') else ''),
            'tld': country.get('tld', [''])[0] if country.get('tld') else '',
            'borders': country.get('borders', []),
            'flag': country.get('flags', {}).get('png', ''),
            'maps': country.get('maps', {}).get('googleMaps', ''),
            'driving_side': country.get('car', {}).get('side', ''),
            'start_of_week': country.get('startOfWeek', 'monday')
        }
