"""
AI Service (using Google Gemini)
Handles all interactions with Google's Gemini API
"""
import google.generativeai as genai
from config import Config
import logging

logger = logging.getLogger(__name__)

class ClaudeService:
    """Service for interacting with AI (now using Google Gemini)"""

    def __init__(self):
        # Configure Gemini API
        genai.configure(api_key=Config.GEMINI_API_KEY)

        # Use Gemini 2.0 Flash (fast and free)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def generate_travel_advice(self, user_input, weather_data, country_data):
        """
        Generate comprehensive travel advice based on user input and data

        Args:
            user_input: Dictionary with destination, dates, preferences, etc.
            weather_data: Weather forecast data
            country_data: Country information (currency, language, etc.)

        Returns:
            Dictionary with comprehensive travel advice
        """
        prompt = self._build_travel_prompt(user_input, weather_data, country_data)

        try:
            logger.info(f"Generating travel advice for {user_input.get('destination')}")

            # Generate content using Gemini
            response = self.model.generate_content(prompt)

            response_text = response.text

            # Parse the response into structured sections
            advice = self._parse_advice_response(response_text)

            # Add power adapter information with images
            advice['power_adapter'] = self._get_power_adapter_info(country_data, response_text)

            logger.info("Travel advice generated successfully")
            return advice

        except Exception as e:
            logger.error(f"Error generating travel advice: {str(e)}")
            raise

    def _build_travel_prompt(self, user_input, weather_data, country_data):
        """Build the prompt for Gemini"""

        destination = user_input.get('destination', '')
        dates = user_input.get('dates', {})
        purpose = user_input.get('purpose', '')
        travelers = user_input.get('travelers', {})
        food_prefs = user_input.get('food_preferences', [])
        accommodation = user_input.get('accommodation', {})
        specific_questions = user_input.get('specific_questions', '')

        prompt = f"""You are an expert travel advisor. Provide comprehensive, practical travel advice for the following trip:

TRIP DETAILS:
- Destination: {destination}
- Travel Dates: {dates.get('start')} to {dates.get('end')}
- Duration: {dates.get('duration_days')} days
- Purpose: {purpose}

TRAVELER PROFILE:
- Type: {travelers.get('type', 'Individual')}
- Number of travelers: {travelers.get('count', 1)}
- Group composition: {travelers.get('composition', 'N/A')}
- Ages: {travelers.get('age_range', 'Not specified')}

PREFERENCES:
- Food Preferences/Restrictions: {', '.join(food_prefs) if food_prefs else 'None specified'}
- Accommodation Type: {accommodation.get('type', 'Not specified')}
- Accommodation Location: {accommodation.get('location', 'Not specified')}
- Budget: {accommodation.get('budget', 'Not specified')}

WEATHER FORECAST:
{self._format_weather_data(weather_data)}

COUNTRY INFORMATION:
{self._format_country_data(country_data)}

SPECIFIC QUESTIONS:
{specific_questions if specific_questions else 'None'}

Please provide detailed advice in the following sections. Use clear headers and bullet points:

1. ACCOMMODATION RECOMMENDATIONS
   - Recommend specific areas to stay based on their preferences
   - Suggest types of accommodation (hotels, Airbnb, hostels, etc.)
   - Budget considerations
   - Booking tips

2. CURRENCY & PAYMENTS
   - Local currency details
   - Should they carry cash or rely on cards?
   - Is mobile payment (Apple Pay, Google Pay) widely accepted?
   - Where to exchange money
   - Typical costs for meals, transport, activities

3. TRANSPORTATION
   - PUBLIC TRANSPORT: How it works, payment methods, advisability
   - CAR RENTAL: Process, cost, advisability, driving tips
   - TAXIS/RIDE-SHARING: How they work, apps to use, typical costs
   - Getting from airport to city
   - Best way to get around based on their itinerary

4. CULTURAL GUIDE
   - TIPPING CULTURE: Where, when, how much
   - DRESS CODE: What to wear, cultural considerations
   - LOCAL CUSTOMS: Important etiquette, do's and don'ts
   - GREETINGS: Essential phrases in local language with pronunciation
   - CULTURAL SENSITIVITIES: Things to avoid or be aware of

5. FOOD & DINING
   - Must-try local dishes
   - Restaurant recommendations fitting their preferences
   - Where to find specific cuisine types
   - Dietary restriction considerations
   - Street food safety
   - Tipping at restaurants

6. ACTIVITIES & ATTRACTIONS
   - Top recommendations based on their purpose and traveler profile
   - Hidden gems
   - Day trip options
   - Activity costs and booking tips
   - What to do in bad weather

7. PRACTICAL INFORMATION
   - POWER ADAPTERS: Type needed, voltage
   - SIM CARDS: Where to buy, recommended providers, costs
   - EMERGENCY CONTACTS: Police, ambulance, tourist police
   - LANGUAGE: How much English is spoken
   - INTERNET: WiFi availability, data options
   - SAFETY: General safety level, areas to avoid, common scams

8. PACKING RECOMMENDATIONS
   - Clothing based on weather and activities
   - Essential items to bring
   - Things you can buy there vs. bring from home
   - Prohibited items

9. SAFETY & HEALTH
   - General safety tips
   - Common scams to watch for
   - Health precautions
   - Water safety
   - Areas to avoid

10. ANSWERS TO SPECIFIC QUESTIONS
    {f"- {specific_questions}" if specific_questions else "- None provided"}

Please be specific, practical, and realistic. Include actual costs where relevant (in local currency and USD). Make recommendations tailored to their travel profile and purpose."""

        return prompt

    def _format_weather_data(self, weather_data):
        """Format weather data for prompt"""
        if not weather_data:
            return "Weather data not available"

        formatted = []
        for day in weather_data.get('forecast', []):
            formatted.append(
                f"- {day.get('date')}: {day.get('condition')}, "
                f"High: {day.get('temp_max')}°C, Low: {day.get('temp_min')}°C, "
                f"Rain: {day.get('rain_chance')}%"
            )

        return '\n'.join(formatted) if formatted else "No forecast available"

    def _format_country_data(self, country_data):
        """Format country data for prompt"""
        if not country_data:
            return "Country data not available"

        return f"""- Currency: {country_data.get('currency', 'N/A')}
- Languages: {', '.join(country_data.get('languages', []))}
- Capital: {country_data.get('capital', 'N/A')}
- Region: {country_data.get('region', 'N/A')}
- Timezone: {country_data.get('timezone', 'N/A')}"""

    def _get_power_adapter_info(self, country_data, response_text):
        """Extract power adapter info and provide helpful URL"""

        # Build country-specific URL
        country_name = country_data.get('name', '') if country_data else ''

        logger.info(f"Building power adapter URL - Country data: {country_data}")
        logger.info(f"Country name extracted: '{country_name}'")

        if country_name:
            # Convert country name to URL format (lowercase, replace spaces with hyphens)
            country_slug = country_name.lower().replace(' ', '-')
            # Remove special characters
            country_slug = ''.join(c if c.isalnum() or c == '-' else '' for c in country_slug)
            info_url = f'https://www.worldstandards.eu/electricity/plug-voltage-by-country/{country_slug}/'
            logger.info(f"Generated country-specific URL: {info_url}")
        else:
            # Fallback to general page
            info_url = 'https://www.worldstandards.eu/electricity/plugs-and-sockets/'
            logger.info(f"Using fallback URL (no country name): {info_url}")

        adapter_info = {
            'description': '',
            'info_url': info_url
        }

        # Extract description (look for POWER ADAPTERS section)
        lines = response_text.split('\n')
        in_power_section = False
        for line in lines:
            if 'POWER ADAPTER' in line.upper():
                in_power_section = True
                continue
            elif in_power_section and line.strip().startswith('-'):
                adapter_info['description'] += line.strip() + ' '
            elif in_power_section and line.strip() and not line.strip().startswith('-'):
                if any(keyword in line.upper() for keyword in ['SIM', 'EMERGENCY', 'LANGUAGE']):
                    break

        return adapter_info

    def _parse_advice_response(self, response_text):
        """Parse AI response into structured sections"""

        sections = {
            'accommodation': '',
            'currency_payments': '',
            'transportation': '',
            'cultural_guide': '',
            'food_dining': '',
            'activities': '',
            'practical_info': '',
            'packing': '',
            'safety_health': '',
            'specific_answers': '',
            'full_text': response_text
        }

        # Improved parsing with better section detection
        current_section = None
        lines = response_text.split('\n')

        for line in lines:
            line_upper = line.upper()
            line_stripped = line_upper.strip()

            # Check for section headers (with or without numbers)
            # Match patterns like "1. ACCOMMODATION" or "ACCOMMODATION RECOMMENDATIONS"
            if ('1.' in line_stripped or '1)' in line_stripped) and 'ACCOMMODATION' in line_upper:
                current_section = 'accommodation'
                continue
            elif ('2.' in line_stripped or '2)' in line_stripped) and 'CURRENCY' in line_upper:
                current_section = 'currency_payments'
                continue
            elif ('3.' in line_stripped or '3)' in line_stripped) and 'TRANSPORTATION' in line_upper:
                current_section = 'transportation'
                continue
            elif ('4.' in line_stripped or '4)' in line_stripped) and ('CULTURAL' in line_upper or 'CULTURE' in line_upper):
                current_section = 'cultural_guide'
                continue
            elif ('5.' in line_stripped or '5)' in line_stripped) and 'FOOD' in line_upper:
                current_section = 'food_dining'
                continue
            elif ('6.' in line_stripped or '6)' in line_stripped) and ('ACTIVITIES' in line_upper or 'ATTRACTIONS' in line_upper):
                current_section = 'activities'
                continue
            elif ('7.' in line_stripped or '7)' in line_stripped) and 'PRACTICAL' in line_upper:
                current_section = 'practical_info'
                continue
            elif ('8.' in line_stripped or '8)' in line_stripped) and 'PACKING' in line_upper:
                current_section = 'packing'
                continue
            elif ('9.' in line_stripped or '9)' in line_stripped) and ('SAFETY' in line_upper or 'HEALTH' in line_upper):
                current_section = 'safety_health'
                continue
            elif ('10.' in line_stripped or '10)' in line_stripped) and 'SPECIFIC' in line_upper:
                current_section = 'specific_answers'
                continue

            # Add content to current section
            if current_section and line.strip():
                sections[current_section] += line + '\n'

        return sections
