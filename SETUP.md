# WhatsApp Bot Setup Guide

## Overview
This bot lets parents sign up and manage their kids' sports reports directly from WhatsApp.
It uses the Meta WhatsApp Business Cloud API + Claude for natural language parsing + Supabase for storage.

## Step 1: Meta Business Setup (~15 min)

1. Go to https://developers.facebook.com/ and log in (or create an account)
2. Click "My Apps" → "Create App"
3. Choose "Other" → "Business" → give it a name like "My Sports Report Bot"
4. In the app dashboard, click "Add Product" → find "WhatsApp" → "Set Up"
5. You'll get:
   - A **test phone number** (for sending)
   - A **Phone Number ID** (looks like `123456789012345`)
   - A **temporary access token** (valid 24h — we'll make a permanent one later)
6. Add your personal phone number as a "To" number for testing

**Save these values — you'll need them for environment variables.**

## Step 2: Deploy the Bot

### Option A: Railway (recommended)
1. Go to https://railway.app/ and sign up (GitHub login works)
2. Click "New Project" → "Deploy from GitHub Repo" (or "Empty Project" → "Add Service")
3. If using GitHub: push the `whatsapp-bot/` folder to a repo first
4. If manual: use Railway CLI: `railway up` from the `whatsapp-bot/` directory
5. Add environment variables in the Railway dashboard:
   - `WHATSAPP_VERIFY_TOKEN` = `mysportsreport_verify_2026` (or any string you choose)
   - `WHATSAPP_ACCESS_TOKEN` = (from Meta dashboard)
   - `WHATSAPP_PHONE_ID` = (from Meta dashboard)
   - `ANTHROPIC_API_KEY` = (your existing key)
   - `SUPABASE_URL` = `https://mvihwttjfkengswsopfu.supabase.co`
   - `SUPABASE_SERVICE_KEY` = (your existing key)
6. Railway will give you a public URL like `https://your-app.up.railway.app`

### Option B: Render
1. Go to https://render.com/ and sign up
2. Create a new "Web Service"
3. Connect your GitHub repo or upload the code
4. Set environment variables (same as above)
5. Render gives you a URL like `https://your-app.onrender.com`

## Step 3: Connect the Webhook

1. Go back to the Meta Developer Dashboard → WhatsApp → Configuration
2. Set the **Callback URL** to: `https://YOUR-DEPLOYED-URL/webhook`
3. Set the **Verify Token** to the same value you used for `WHATSAPP_VERIFY_TOKEN`
4. Click "Verify and Save" — Meta will hit your `/webhook` GET endpoint
5. Subscribe to the "messages" webhook field

## Step 4: Test It!

Send a WhatsApp message to your test number:
> "Hey, I want to sign up my son Marcus. He loves the Lakers."

The bot should reply, ask for an email, and create the subscriber in Supabase.

## Step 5: Permanent Access Token

The temporary token expires after 24h. To get a permanent one:
1. In Meta Developer Dashboard → WhatsApp → API Setup
2. Click "Generate" under System User token
3. Or create a System User in Business Settings → System Users → Generate Token
   - Select your app and grant `whatsapp_business_messaging` permission
4. Replace the temporary token in your environment variables

## Step 6: Go Live (Optional)

By default, you can only message phone numbers you've added to the test list.
To allow anyone to message your bot:
1. Go to Meta App Dashboard → App Review
2. Submit your app for review with `whatsapp_business_messaging` permission
3. Once approved, add a real business phone number

## Environment Variables Reference

| Variable | Description |
|----------|-------------|
| `WHATSAPP_VERIFY_TOKEN` | Any string you choose for webhook verification |
| `WHATSAPP_ACCESS_TOKEN` | Meta API token (from developer dashboard) |
| `WHATSAPP_PHONE_ID` | Your WhatsApp phone number ID |
| `ANTHROPIC_API_KEY` | Claude API key |
| `SUPABASE_URL` | Your Supabase project URL |
| `SUPABASE_SERVICE_KEY` | Supabase service role key |

## Testing Locally

```bash
cd whatsapp-bot
pip install -r requirements.txt
export ANTHROPIC_API_KEY="your-key"
export SUPABASE_SERVICE_KEY="your-key"
python app.py
```

Then use ngrok to expose your local server:
```bash
ngrok http 5000
```

Use the ngrok URL as your webhook URL in the Meta dashboard.

## Example Conversations

**New signup:**
> User: Hi! I want to sign up my daughter Sofia for NBA reports
> Bot: Hey! 🏀 Sofia's gonna love it! Which NBA team is her favorite?
> User: She's obsessed with the Celtics
> Bot: Great taste! I'll set her up with Celtics box scores, NBA scores, standings, and more. What's your email so we can deliver the report?
> User: maria@gmail.com
> Bot: Done! ✅ Sofia's Celtics report is all set. She'll get her first report tomorrow morning. Print it out and leave it on the kitchen table!
> 📎 Edit anytime: https://mydailysportsreport.com/signup.html?id=abc123

**Edit existing:**
> User: Can you add Premier League to Sofia's report?
> Bot: Added! ⚽ Sofia will now get Premier League results and standings alongside her NBA stuff.

**Quick signup:**
> User: Sign up Jake, jake.dad@email.com, Knicks fan, also wants MLS Inter Miami
> Bot: Done! ✅ Jake is set up with Knicks NBA coverage + Inter Miami MLS. First report arrives tomorrow!
