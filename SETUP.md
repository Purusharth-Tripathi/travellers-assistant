# Setup Guide - Traveller's Assistant App

Follow these steps to get your Traveller's Assistant app up and running!

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A text editor or IDE
- Internet connection

## Step-by-Step Setup

### 1. Get Your API Keys (15 minutes)

Before starting, you'll need API keys. Follow the detailed instructions in `API_GUIDE.md`.

**Minimum Required:**
- ✅ Anthropic Claude API key
- ✅ OpenWeatherMap API key

### 2. Navigate to Project Directory

Open your terminal/command prompt and navigate to the project folder:

```bash
cd path/to/travellers-assistant
```

### 3. Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### 4. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- Anthropic SDK (Claude AI)
- Requests (API calls)
- Flask-CORS (cross-origin requests)
- python-dotenv (environment variables)

### 5. Configure Environment Variables

```bash
# Go back to root directory
cd ..

# Copy the example file
cp .env.example .env
```

Now edit `.env` file and add your API keys:

```bash
# Open in your text editor
notepad .env  # Windows
nano .env     # Mac/Linux
```

Add your keys:
```
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
OPENWEATHER_API_KEY=your-actual-key-here
```

Save and close the file.

### 6. Verify Configuration

Test if your API keys are configured correctly:

```bash
cd backend
python app.py
```

You should see:
```
Configuration validated successfully
Starting Traveller's Assistant on port 5000
```

If you see errors about missing API keys, double-check your `.env` file.

### 7. Open the App

Open your web browser and go to:
```
http://localhost:5000
```

You should see the Traveller's Assistant interface!

### 8. Test It Out

Try creating a travel plan:
1. Enter destination: "Paris, France"
2. Select dates: Next week for 5 days
3. Fill in your preferences
4. Click "Generate Travel Plan"

The app will take 15-30 seconds to generate your personalized plan.

## Troubleshooting

### "Module not found" Error

**Problem:** Python can't find the installed packages.

**Solution:**
```bash
# Make sure virtual environment is activated
# You should see (venv) in your prompt

# Reinstall dependencies
pip install -r backend/requirements.txt
```

### "Invalid API Key" Error

**Problem:** API key is incorrect or not set.

**Solutions:**
1. Check `.env` file is in the root directory (same level as backend folder)
2. Verify API keys have no extra spaces or quotes
3. For OpenWeatherMap: Wait 2 hours for new keys to activate
4. Try copying the key again from the provider's website

### "Connection Refused" Error

**Problem:** Backend server isn't running.

**Solution:**
```bash
cd backend
python app.py
```

Keep this terminal window open while using the app.

### "CORS Error" in Browser Console

**Problem:** Frontend can't connect to backend.

**Solution:**
1. Make sure backend is running on port 5000
2. Check that flask-cors is installed:
   ```bash
   pip install flask-cors
   ```
3. Restart the backend server

### Weather Data Not Loading

**Problem:** OpenWeatherMap API isn't working.

**Solutions:**
1. New API keys take up to 2 hours to activate
2. Check you haven't exceeded free tier limit (1000 calls/day)
3. Verify the API key in `.env` is correct

### Slow Response Times

**Problem:** Travel plan generation takes too long.

**Explanation:** This is normal! Claude AI takes 15-30 seconds to generate comprehensive advice. The more detailed your input, the longer it takes.

## Running in Production

### Option 1: Local Network Access

To access from other devices on your network:

```bash
# In backend/app.py, the server already runs on 0.0.0.0
# Just find your computer's local IP address

# Windows
ipconfig

# Mac/Linux  
ifconfig
```

Look for your IP (e.g., 192.168.1.100), then access from other devices:
```
http://192.168.1.100:5000
```

### Option 2: Deploy Online (Free)

Deploy to Vercel, Heroku, or Railway for free online access. See deployment guides in the documentation.

## Daily Usage

### Starting the App

Every time you want to use the app:

1. Open terminal
2. Navigate to project:
   ```bash
   cd path/to/travellers-assistant
   ```
3. Activate virtual environment:
   ```bash
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Mac/Linux
   ```
4. Start server:
   ```bash
   cd backend
   python app.py
   ```
5. Open browser to `http://localhost:5000`

### Stopping the App

Press `Ctrl+C` in the terminal running the server.

## Cost Monitoring

Track your API usage:

**Anthropic Claude:**
- Check usage: https://console.anthropic.com/settings/usage
- Free tier: $5 credit
- Typical cost: $0.003 per travel plan

**OpenWeatherMap:**
- Check usage: https://home.openweathermap.org/statistics
- Free tier: 1000 calls/day
- You'll likely never exceed this

## Security Best Practices

1. ✅ Never commit `.env` file to Git
2. ✅ Don't share your API keys
3. ✅ Use environment variables in production
4. ✅ Rotate keys if accidentally exposed
5. ✅ Keep dependencies updated

## Getting Help

### In Claude Code

Open the project in Claude Code and ask me for help:
```
I'm getting [error message]. Can you help me fix it?
```

### Check Logs

If something's not working, check the terminal where the server is running for error messages.

### Common Issues Document

See `TROUBLESHOOTING.md` for more detailed solutions.

## Next Steps

1. ✅ Customize the app for your needs
2. ✅ Add more features (see README.md for Phase 2 ideas)
3. ✅ Share with friends and family
4. ✅ Deploy online for access anywhere

## Need More Help?

Open this project in Claude Code and I'll walk you through any issues step-by-step!

Happy travels! 🌍✈️
