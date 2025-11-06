# API Setup Guide 🔑

This guide will walk you through getting all the API keys needed for the Traveller's Assistant App.

## Priority Order

1. **Anthropic Claude API** (Essential) - Powers the intelligent recommendations
2. **OpenWeatherMap** (Essential) - Weather forecasts
3. **REST Countries** (No key needed) - Country information
4. **ExchangeRate-API** (Optional) - Currency rates
5. **Google Places** (Optional) - Enhanced accommodation search

---

## 1. Anthropic Claude API (ESSENTIAL)

This is the brain of your app - it generates all the intelligent travel advice.

### Signup Process
1. Go to: https://console.anthropic.com/
2. Click "Sign Up" (top right)
3. Use your email or Google account
4. Verify your email

### Get Your API Key
1. Once logged in, go to "API Keys" in the sidebar
2. Click "Create Key"
3. Give it a name: "Travellers Assistant"
4. Copy the key (starts with `sk-ant-...`)
5. **IMPORTANT**: Save it immediately - you can't see it again!

### Pricing
- **Free Credit**: $5 on signup
- **Usage**: ~$0.003 per travel plan (very cheap!)
- **Your $5 gets you**: ~1,600 travel plans
- **After free credit**: Pay-as-you-go

### Add to Your App
In your `.env` file:
```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

---

## 2. OpenWeatherMap API (ESSENTIAL)

Provides accurate weather forecasts for any destination.

### Signup Process
1. Go to: https://openweathermap.org/api
2. Click "Sign Up" (top right)
3. Fill in your details
4. Verify your email

### Get Your API Key
1. After login, click your username (top right)
2. Select "My API Keys"
3. You'll see a default key already created
4. Copy it (or create a new one)

### Pricing
- **Free Tier**: 1,000 API calls per day
- **Cost**: Completely free for your usage
- **Limits**: 60 calls/minute

### Add to Your App
In your `.env` file:
```
OPENWEATHER_API_KEY=your-key-here
```

### API Activation
⚠️ **Important**: New API keys take 10 minutes to 2 hours to activate. Don't worry if it doesn't work immediately!

---

## 3. REST Countries API (NO KEY NEEDED!)

Provides country information like currency, languages, timezones.

### Setup
No signup needed! Just use the API directly:
- **URL**: https://restcountries.com/v3.1/all
- **Free**: Completely free, no limits
- **Data**: Currency, languages, capital, population, etc.

The app will use this automatically - no configuration needed!

---

## 4. ExchangeRate-API (OPTIONAL)

Real-time currency exchange rates.

### Signup Process
1. Go to: https://www.exchangerate-api.com/
2. Click "Get Free Key"
3. Enter your email
4. Check your email for the API key

### Pricing
- **Free Tier**: 1,500 requests per month
- **Perfect for**: Personal travel planning
- **Upgrade**: $9/month for 100,000 requests (overkill for you)

### Add to Your App
In your `.env` file:
```
EXCHANGE_RATE_API_KEY=your-key-here
```

### Alternative
If you don't want to use this, the app will use REST Countries' static exchange rates instead.

---

## 5. Google Places API (OPTIONAL - Advanced)

Enhanced hotel and restaurant search with reviews and photos.

### Signup Process
1. Go to: https://console.cloud.google.com/
2. Create a new project: "Travellers Assistant"
3. Enable "Places API"
4. Go to "Credentials" → "Create Credentials" → "API Key"

### Pricing
- **Free Tier**: $200 credit per month
- **Cost**: $0.017 per Places search
- **Your credit gets**: ~11,700 searches/month
- **Realistically**: You'll never hit the limit

### Add to Your App
In your `.env` file:
```
GOOGLE_PLACES_API_KEY=your-key-here
```

### Restrict Your Key (Security)
1. In Google Cloud Console, click your API key
2. Under "API restrictions" → Select "Restrict key"
3. Choose "Places API"
4. Under "Application restrictions" → Select "HTTP referrers"
5. Add: `http://localhost:5000/*` (for development)

---

## Summary: What You Need

### Minimum (App will work)
- ✅ Anthropic Claude API
- ✅ OpenWeatherMap API
- ✅ REST Countries (no key needed)

### Recommended (Better experience)
- ✅ All of the above
- ✅ ExchangeRate-API

### Optional (Enhanced features)
- ✅ Everything above
- ✅ Google Places API

---

## Your .env File Should Look Like This

```bash
# Essential
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxx
OPENWEATHER_API_KEY=xxxxxxxxxxxxxxxxx

# Optional
EXCHANGE_RATE_API_KEY=xxxxxxxxxxxxxxxxx
GOOGLE_PLACES_API_KEY=xxxxxxxxxxxxxxxxx

# App Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-random-secret-key-here
```

---

## Cost Calculator

Let's say you plan trips for yourself and friends:

**Monthly Usage Estimate**:
- 20 travel plans created
- 20 weather checks
- 20 currency lookups
- 50 accommodation searches

**Monthly Cost**:
- Anthropic Claude: $0.06 (20 × $0.003)
- OpenWeatherMap: $0.00 (free tier)
- ExchangeRate: $0.00 (free tier)
- Google Places: $0.85 (50 × $0.017)

**Total: ~$0.91/month** 💰

For personal use, you'll likely stay completely free!

---

## Troubleshooting

### "Invalid API Key" Error
- Check for typos (copy-paste the entire key)
- Make sure there are no extra spaces
- For OpenWeatherMap: Wait 2 hours for activation

### "Rate Limit Exceeded"
- You're making too many requests
- Wait a few minutes and try again
- Check if you're in a loop accidentally

### "API Key Not Found in Environment"
- Make sure `.env` file is in the root directory
- Restart your Flask app after adding keys
- Check `.env` syntax (no quotes around values)

---

## Security Best Practices

1. ✅ **Never** commit `.env` to Git
2. ✅ Add `.env` to `.gitignore`
3. ✅ Use environment variables in production
4. ✅ Rotate keys if accidentally exposed
5. ✅ Set up API key restrictions where possible

---

## Next Steps

Once you have your keys:
1. Copy `.env.example` to `.env`
2. Add your API keys to `.env`
3. Run `python backend/app.py`
4. Visit `http://localhost:5000`
5. Start planning trips! 🎉

Need help? Open the project in Claude Code and I'll guide you through any issues!
