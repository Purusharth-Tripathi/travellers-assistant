# Traveller's Assistant App 🌍✈️

A comprehensive mobile-friendly web application that helps travelers prepare for their trips with personalized recommendations and essential information.

## Features

### Input Collection
- Destination and travel dates
- Purpose of visit (leisure, business, family event)
- Traveler profiles (individual, group, family, friends, business)
- Food preferences and dietary restrictions
- Accommodation preferences (location, type, budget)
- Specific information requests

### Output Information
- **Weather Forecast** - Detailed weather for travel dates
- **Accommodation** - Recommendations based on preferences and budget
- **Currency & Payments** - Local currency info, cash vs. card guidance
- **Transportation** - Public transport, car rentals, taxis, payment methods
- **Cultural Guide** - Tipping culture, dress code, local customs
- **Food Options** - Restaurant recommendations respecting dietary needs
- **Language Basics** - Common phrases and local greetings
- **Safety Tips** - What to avoid and watch out for
- **Activities** - Personalized recommendations based on traveler profile
- **Practical Info** - Power adapters, SIM cards, emergency contacts
- **Custom Queries** - Answers to specific traveler questions

## Technology Stack

- **Frontend**: HTML5, CSS3 (Tailwind CSS), Vanilla JavaScript
- **Backend**: Python Flask
- **AI**: Anthropic Claude API (for intelligent responses)
- **APIs**: 
  - OpenWeatherMap (weather data)
  - REST Countries (country information)
  - Optional: Google Places, Amadeus Travel APIs

## Recommended API Keys (All Have Free Tiers!)

### 1. Anthropic Claude API (Primary - for intelligent travel advice)
- **URL**: https://console.anthropic.com/
- **Free Tier**: $5 credit on signup
- **Cost**: ~$0.003 per request (very affordable)
- **Why**: Powers the intelligent recommendations and answers

### 2. OpenWeatherMap (Weather forecasts)
- **URL**: https://openweathermap.org/api
- **Free Tier**: 1,000 calls/day
- **Cost**: Free for basic usage
- **Why**: Accurate weather forecasts for travel dates

### 3. REST Countries API (Country data)
- **URL**: https://restcountries.com/
- **Free Tier**: Completely free, no key needed
- **Why**: Currency, language, timezone info

### 4. ExchangeRate-API (Currency conversion - Optional)
- **URL**: https://www.exchangerate-api.com/
- **Free Tier**: 1,500 requests/month
- **Why**: Real-time currency exchange rates

### 5. Google Places API (Optional - for accommodation)
- **URL**: https://developers.google.com/maps/documentation/places/web-service
- **Free Tier**: $200 credit/month
- **Why**: Hotel and restaurant recommendations

## Project Structure

```
travellers-assistant/
├── backend/
│   ├── app.py                    # Flask application
│   ├── config.py                 # Configuration and API keys
│   ├── requirements.txt          # Python dependencies
│   ├── services/
│   │   ├── __init__.py
│   │   ├── claude_service.py     # Claude AI integration
│   │   ├── weather_service.py    # Weather API integration
│   │   ├── country_service.py    # Country information
│   │   └── travel_advisor.py     # Core travel advice logic
│   └── utils/
│       ├── __init__.py
│       └── helpers.py            # Helper functions
├── frontend/
│   ├── index.html                # Main page
│   ├── styles.css                # Custom styles
│   ├── script.js                 # Frontend logic
│   └── assets/
│       └── images/               # Icons and images
├── .env.example                  # Environment variables template
├── README.md                     # This file
├── SETUP.md                      # Setup instructions
└── API_GUIDE.md                  # Detailed API setup guide
```

## Quick Start

### Step 1: Get API Keys (5 minutes)
1. Sign up for Anthropic Claude API
2. Sign up for OpenWeatherMap
3. (Optional) Sign up for ExchangeRate-API

### Step 2: Setup (in Claude Code)
```bash
cd travellers-assistant
pip install -r backend/requirements.txt
```

### Step 3: Configure
```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your API keys
```

### Step 4: Run
```bash
python backend/app.py
```

Open your browser to `http://localhost:5000`

## Features Breakdown

### Phase 1 (MVP) ✅
- User input form (destination, dates, preferences)
- Weather forecast
- Basic country information (currency, language)
- AI-powered travel advice
- Mobile-responsive design

### Phase 2 (Enhanced)
- Accommodation search integration
- Real-time currency conversion
- Interactive maps
- Save/export itinerary as PDF
- Multi-language support

### Phase 3 (Advanced)
- User accounts and saved trips
- Collaborative trip planning
- Budget tracking
- Booking integration
- Offline mode

## Mobile-First Design

The app is designed mobile-first with:
- Responsive layout (works on all screen sizes)
- Touch-friendly buttons and inputs
- Fast loading times
- Progressive Web App (PWA) capabilities
- Works offline (cached responses)

## Cost Estimate

With moderate usage (10-20 trips planned per month):
- **Anthropic Claude**: $0.50 - $1.00/month
- **OpenWeatherMap**: Free
- **REST Countries**: Free
- **Total**: < $1/month

Very affordable for personal use!

## Security

- API keys stored in environment variables (never in code)
- Backend proxy for API calls (keys not exposed to frontend)
- Rate limiting to prevent abuse
- Input validation and sanitization

## Browser Support

- Chrome/Edge (recommended)
- Safari
- Firefox
- Mobile browsers (iOS Safari, Chrome Mobile)

## Next Steps

1. Get your API keys (see API_GUIDE.md)
2. Follow SETUP.md for detailed setup
3. Open in Claude Code for customization
4. Deploy to Vercel/Netlify (free hosting!)

## License

MIT License - Free to use and modify

---

Built with ❤️ for travelers by travelers
