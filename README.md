# Garmin MCP Server for Poke

A Poke-compatible MCP server exposing 95+ Garmin Connect tools over HTTP. Deployable to Render.

## Setup

### 1. Generate OAuth Tokens

Garmin accounts with MFA require local token generation:

```bash
pip install garminconnect garth
python scripts/generate_tokens.py
```

This will prompt for your Garmin email, password, and MFA code, then output a base64 token string.

### 2. Deploy to Render

1. Push this repo to GitHub
2. Create a new Web Service on [Render](https://render.com) pointing to this repo
3. Set environment variables:
   - `GARMINTOKENS_BASE64` = the token string from step 1
4. Deploy

### 3. Connect Poke

Add the Render URL to Poke as an MCP server endpoint:
```
https://your-service.onrender.com/mcp
```

## Local Development

```bash
pip install -r requirements.txt
export GARMINTOKENS_BASE64="your-token-string"
python src/server.py
```

The server runs at `http://localhost:8000/mcp`.

## Token Refresh

Tokens last approximately 6 months. When they expire, re-run `generate_tokens.py` and update the Render env var.

## Tool Categories

| Category | Tools | Examples |
|----------|-------|---------|
| Activity Management | 14 | Activities by date, splits, weather, HR zones, gear |
| Health & Wellness | 28 | Stats, sleep, stress, body battery, HRV, SpO2, steps |
| Training | 10 | Training status, endurance score, hill score, lactate threshold |
| User Profile | 4 | Profile info, settings, unit system |
| Devices | 7 | Device list, settings, alarms, solar data |
| Gear Management | 3 | Gear inventory, add/remove gear from activities |
| Weight Management | 5 | Weigh-ins, add/delete measurements |
| Challenges | 10 | Goals, badges, challenges, race predictions, PRs |
| Workouts | 7 | Workout library, scheduling, training plans, upload |
| Data Management | 3 | Body composition, blood pressure, hydration |
| Women's Health | 3 | Pregnancy, menstrual cycle tracking |
| Workout Templates | 5 | Resources with workout JSON templates |
