# Deployment Guide

## Deploy to Render (Recommended - Free Tier Available)

### Prerequisites
- GitHub account with your code pushed
- Google Gemini API key
- OpenWeatherMap API key

### Steps

1. **Sign up for Render**
   - Go to https://render.com
   - Sign up with your GitHub account

2. **Create a New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select `travellers-assistant` repository

3. **Configure Service**
   - **Name**: `travellers-assistant` (or your preferred name)
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python backend/app.py`

4. **Add Environment Variables**
   Click "Advanced" → "Add Environment Variable" for each:
   ```
   GEMINI_API_KEY=your_gemini_key_here
   OPENWEATHER_API_KEY=your_openweather_key_here
   EXCHANGE_RATE_API_KEY=your_exchange_rate_key_here
   GOOGLE_PLACES_API_KEY=your_google_places_key_here
   PORT=10000
   DEBUG=False
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Your app will be live at: `https://your-app-name.onrender.com`

6. **Update Frontend**
   - After deployment, update `frontend/script-v3.js` line 3:
   ```javascript
   const API_BASE_URL = 'https://your-app-name.onrender.com/api';
   ```
   - Commit and push changes

## Deploy to Railway (Alternative)

1. **Sign up for Railway**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project" → "Deploy from GitHub repo"
   - Select `travellers-assistant`

3. **Add Environment Variables**
   - Go to Variables tab
   - Add all API keys from `.env` file

4. **Deploy**
   - Railway auto-detects Python and deploys
   - Get your public URL from the Deployments tab

## Deploy to Heroku

1. **Install Heroku CLI**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Heroku App**
   ```bash
   heroku login
   heroku create your-app-name
   ```

3. **Add Buildpack**
   ```bash
   heroku buildpacks:set heroku/python
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set GEMINI_API_KEY=your_key_here
   heroku config:set OPENWEATHER_API_KEY=your_key_here
   heroku config:set EXCHANGE_RATE_API_KEY=your_key_here
   heroku config:set GOOGLE_PLACES_API_KEY=your_key_here
   ```

5. **Create Procfile**
   Create `Procfile` in root directory:
   ```
   web: python backend/app.py
   ```

6. **Deploy**
   ```bash
   git push heroku main
   ```

## Important Notes

### CORS Configuration
When deploying, you may need to update CORS settings in `backend/app.py`:

```python
# For production, specify your frontend domain
CORS(app, origins=["https://your-domain.com"])
```

### Port Configuration
Most platforms (Render, Railway, Heroku) provide a PORT environment variable.
Your `backend/config.py` already handles this:
```python
PORT = int(os.getenv('PORT', 5000))
```

### API Rate Limits
- **Gemini API**: Free tier has rate limits
- **OpenWeatherMap**: 1000 calls/day on free tier
- **Open-Meteo**: No API key needed, generous limits

### Security Checklist
✅ `.env` file is in `.gitignore`
✅ API keys are set as environment variables
✅ DEBUG mode is off in production
✅ CORS is configured properly

## Testing Your Deployment

1. Visit your deployed URL
2. Try generating a travel plan
3. Check browser console for errors
4. Test the follow-up questions feature
5. Verify power adapter links work

## Troubleshooting

### App won't start
- Check logs: `heroku logs --tail` (Heroku) or check Render/Railway dashboard
- Verify all environment variables are set
- Ensure `requirements.txt` includes all dependencies

### CORS errors
- Update CORS configuration in `backend/app.py`
- Add your frontend domain to allowed origins

### API errors
- Verify API keys are correct
- Check API quotas/limits
- Review API documentation for changes

## Cost Considerations

**Free Tier Options:**
- **Render**: Free tier with 750 hours/month (sleeps after 15 min inactivity)
- **Railway**: $5/month credit free
- **Heroku**: No longer offers free tier

**API Costs:**
- **Google Gemini**: Free tier available
- **OpenWeatherMap**: Free up to 1000 calls/day
- **REST Countries API**: Completely free
- **Open-Meteo**: Free

## Custom Domain (Optional)

1. Buy a domain (Namecheap, Google Domains, etc.)
2. In your deployment platform:
   - Go to Settings → Custom Domain
   - Add your domain
   - Update DNS records as instructed

## Monitoring

- Set up uptime monitoring: https://uptimerobot.com
- Monitor API usage in respective dashboards
- Check deployment platform logs regularly
