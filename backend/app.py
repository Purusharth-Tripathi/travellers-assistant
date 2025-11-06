"""
Traveller's Assistant App - Flask Backend
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import logging
import os

from config import Config
from services import ClaudeService, WeatherService, CountryService

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, static_folder='../frontend', static_url_path='')
app.config.from_object(Config)
CORS(app)

# Initialize services
claude_service = ClaudeService()
weather_service = WeatherService()
country_service = CountryService()

@app.route('/')
def index():
    """Serve the main page"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/validate-config', methods=['GET'])
def validate_config():
    """Validate API configuration"""
    try:
        Config.validate_config()
        return jsonify({
            'valid': True,
            'message': 'Configuration is valid',
            'apis': {
                'gemini': bool(Config.GEMINI_API_KEY),
                'openweather': bool(Config.OPENWEATHER_API_KEY),
                'exchangerate': bool(Config.EXCHANGE_RATE_API_KEY),
                'google_places': bool(Config.GOOGLE_PLACES_API_KEY)
            }
        })
    except ValueError as e:
        return jsonify({
            'valid': False,
            'message': str(e)
        }), 400

@app.route('/api/generate-plan', methods=['POST'])
def generate_travel_plan():
    """
    Generate comprehensive travel plan
    
    Expected JSON payload:
    {
        "destination": "Paris, France",
        "dates": {
            "start": "2024-06-01",
            "end": "2024-06-10"
        },
        "purpose": "leisure",
        "travelers": {
            "type": "family",
            "count": 4,
            "composition": "2 adults, 2 children (ages 8, 12)",
            "age_range": "8-45"
        },
        "food_preferences": ["vegetarian", "no nuts"],
        "accommodation": {
            "type": "hotel",
            "location": "city center",
            "budget": "mid-range"
        },
        "specific_questions": "Best family-friendly restaurants?"
    }
    """
    try:
        user_input = request.json
        logger.info(f"Generating travel plan for {user_input.get('destination')}")
        
        # Validate required fields
        required = ['destination', 'dates']
        missing = [field for field in required if field not in user_input]
        if missing:
            return jsonify({
                'error': f"Missing required fields: {', '.join(missing)}"
            }), 400
        
        # Calculate duration
        start_date = datetime.strptime(user_input['dates']['start'], '%Y-%m-%d')
        end_date = datetime.strptime(user_input['dates']['end'], '%Y-%m-%d')
        duration = (end_date - start_date).days + 1
        user_input['dates']['duration_days'] = duration
        
        # Extract destination
        destination = user_input['destination']

        # Fetch weather data first (includes country code from geocoding)
        logger.info("Fetching weather data...")
        weather_data = weather_service.get_weather_forecast(
            destination,
            user_input['dates']['start'],
            user_input['dates']['end']
        )

        # Fetch country information using country code from weather data
        logger.info("Fetching country information...")
        country_data = None

        # Try to get country code from weather coordinates
        if weather_data and weather_data.get('coordinates', {}).get('country'):
            country_code = weather_data['coordinates']['country']
            logger.info(f"Using country code from geocoding: {country_code}")
            country_data = country_service.get_country_info_by_code(country_code)

        # Fallback: try to extract country name from destination string
        if not country_data:
            country_name = destination.split(',')[-1].strip() if ',' in destination else destination
            logger.info(f"Fallback: trying country name '{country_name}' from destination")
            country_data = country_service.get_country_info(country_name)
        
        # Generate AI-powered travel advice
        logger.info("Generating AI-powered travel advice...")
        travel_advice = claude_service.generate_travel_advice(
            user_input,
            weather_data,
            country_data
        )
        
        # Compile complete response
        response = {
            'success': True,
            'input': user_input,
            'weather': weather_data,
            'country': country_data,
            'advice': travel_advice,
            'generated_at': datetime.now().isoformat()
        }
        
        logger.info("Travel plan generated successfully")
        return jsonify(response)

    except Exception as e:
        logger.error(f"Error generating travel plan: {str(e)}")
        return jsonify({
            'error': 'Failed to generate travel plan',
            'details': str(e)
        }), 500

@app.route('/api/ask-question', methods=['POST'])
def ask_question():
    """
    Answer follow-up questions about the destination

    Expected JSON payload:
    {
        "question": "What are the best museums to visit?",
        "context": {
            "destination": "Paris",
            "dates": {"start": "2024-06-01", "end": "2024-06-10"},
            "country": "France"
        }
    }
    """
    try:
        data = request.json
        question = data.get('question', '')
        context = data.get('context', {})

        if not question:
            return jsonify({'error': 'Question is required'}), 400

        logger.info(f"Answering question about {context.get('destination')}: {question}")

        # Build prompt for AI
        destination = context.get('destination', 'this destination')
        country = context.get('country', '')
        dates = context.get('dates', {})

        prompt = f"""You are a knowledgeable travel assistant. A traveler is planning a trip to {destination}"""
        if country:
            prompt += f" in {country}"
        if dates.get('start'):
            prompt += f" from {dates.get('start')} to {dates.get('end')}"

        prompt += f""".

They have a question: {question}

Please provide a helpful, practical, and specific answer. Keep it concise (2-4 sentences) but informative."""

        # Get answer from AI
        response = claude_service.model.generate_content(prompt)
        answer = response.text

        logger.info("Question answered successfully")
        return jsonify({
            'success': True,
            'question': question,
            'answer': answer
        })

    except Exception as e:
        logger.error(f"Error answering question: {str(e)}")
        return jsonify({
            'error': 'Failed to answer question',
            'details': str(e)
        }), 500

@app.route('/api/weather/<destination>', methods=['GET'])
def get_weather(destination):
    """Get weather forecast for a destination"""
    try:
        start_date = request.args.get('start')
        end_date = request.args.get('end')
        
        if not start_date or not end_date:
            return jsonify({'error': 'start and end dates required'}), 400
        
        weather_data = weather_service.get_weather_forecast(
            destination,
            start_date,
            end_date
        )
        
        if weather_data:
            return jsonify(weather_data)
        else:
            return jsonify({'error': 'Weather data not available'}), 404
            
    except Exception as e:
        logger.error(f"Error fetching weather: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/country/<country_name>', methods=['GET'])
def get_country(country_name):
    """Get country information"""
    try:
        country_data = country_service.get_country_info(country_name)
        
        if country_data:
            return jsonify(country_data)
        else:
            return jsonify({'error': 'Country not found'}), 404
            
    except Exception as e:
        logger.error(f"Error fetching country info: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    try:
        # Validate configuration
        Config.validate_config()
        logger.info("Configuration validated successfully")
        
        # Start server
        logger.info(f"Starting Traveller's Assistant on port {Config.PORT}")
        app.run(
            host='0.0.0.0',
            port=Config.PORT,
            debug=Config.DEBUG,
            use_reloader=False
        )
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}")
        raise
