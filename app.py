"""
WhatsApp Bot for My Sports Report — webhook server.

Receives WhatsApp messages via the Meta Cloud API, parses them with Claude,
and manages subscriber preferences in Supabase.

Environment variables required:
    WHATSAPP_VERIFY_TOKEN   - Token you set during webhook registration
    WHATSAPP_ACCESS_TOKEN   - Meta API access token
    WHATSAPP_PHONE_ID       - Your WhatsApp Business phone number ID
    ANTHROPIC_API_KEY        - Claude API key
    SUPABASE_URL            - Supabase project URL
    SUPABASE_SERVICE_KEY    - Supabase service role key
"""

import os
import json
import time
import requests
from flask import Flask, request, jsonify

from ai_parser import parse_message
from config import SETTINGS_URL

app = Flask(__name__)

# ── Config ──
VERIFY_TOKEN = os.environ.get("WHATSAPP_VERIFY_TOKEN", "mysportsreport_verify_2026")
ACCESS_TOKEN = os.environ.get("WHATSAPP_ACCESS_TOKEN", "")
PHONE_NUMBER_ID = os.environ.get("WHATSAPP_PHONE_ID", "")
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://mvihwttjfkengswsopfu.supabase.co")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY", "")
ADMIN_PHONE = os.environ.get("ADMIN_PHONE", "")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
GITHUB_REPO = os.environ.get("GITHUB_REPO", "mydailysportsreport-tech/sports-reports")

# In-memory conversation store (keyed by phone number)
# In production, you'd use Redis or Supabase for persistence
conversations = {}
CONVERSATION_TTL = 1800  # 30 minutes

# Deduplication: track recently processed message IDs to ignore webhook retries
processed_messages = {}
DEDUP_TTL = 120  # 2 minutes


# ── WhatsApp API helpers ──

def send_whatsapp_message(to, text):
    """Send a text message via the WhatsApp Cloud API."""
    if not ACCESS_TOKEN or not PHONE_NUMBER_ID:
        print(f"[DRY RUN] To {to}: {text}")
        return

    url = f"https://graph.facebook.com/v21.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text},
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        if resp.status_code != 200:
            print(f"WhatsApp API error: {resp.status_code} {resp.text}")
    except Exception as e:
        print(f"WhatsApp send error: {e}")


# ── Supabase helpers ──

def supabase_headers():
    return {
        "apikey": SUPABASE_SERVICE_KEY,
        "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }


def create_subscriber(data, phone=""):
    """Create a new subscriber in Supabase."""
    url = f"{SUPABASE_URL}/rest/v1/subscribers"
    payload = {
        "name": data["name"],
        "email": data["email"],
        "parent_email": data["email"],
        "color_theme": data.get("color_theme", "blue"),
        "favorite_athlete": data.get("favorite_athlete", ""),
        "sports": data.get("sports", []),
        "phone": phone,
        "active": True,
    }
    resp = requests.post(url, headers=supabase_headers(), json=payload, timeout=15)
    if resp.status_code in (200, 201):
        result = resp.json()
        if isinstance(result, list) and result:
            return result[0]
        return result
    print(f"Supabase create error: {resp.status_code} {resp.text}")
    return None


def lookup_subscribers(email):
    """Look up active subscribers by email."""
    url = f"{SUPABASE_URL}/rest/v1/subscribers?email=eq.{email}&active=eq.true&select=id,name,email,sports,color_theme,favorite_athlete,phone"
    resp = requests.get(url, headers=supabase_headers(), timeout=15)
    if resp.status_code == 200:
        return resp.json()
    return []


def lookup_by_phone(phone):
    """Look up active subscribers by phone number."""
    url = f"{SUPABASE_URL}/rest/v1/subscribers?phone=eq.{phone}&active=eq.true&select=id,name,email,sports,color_theme,favorite_athlete,phone"
    resp = requests.get(url, headers=supabase_headers(), timeout=15)
    if resp.status_code == 200:
        return resp.json()
    return []


def update_subscriber(sub_id, data):
    """Update an existing subscriber in Supabase."""
    url = f"{SUPABASE_URL}/rest/v1/subscribers?id=eq.{sub_id}"
    resp = requests.patch(url, headers=supabase_headers(), json=data, timeout=15)
    return resp.status_code in (200, 204)


def deactivate_subscriber(email=None, name=None):
    """Set active=false for a subscriber."""
    filters = "active=eq.true"
    if email:
        filters += f"&email=eq.{email}"
    if name:
        filters += f"&name=eq.{name}"

    url = f"{SUPABASE_URL}/rest/v1/subscribers?{filters}"
    resp = requests.patch(url, headers=supabase_headers(), json={"active": False}, timeout=15)
    return resp.status_code in (200, 204)


# ── GitHub Actions trigger ──

def trigger_report_for_subscriber(subscriber_id):
    """Dispatch a GitHub Actions workflow to generate and email a single subscriber's report."""
    if not GITHUB_TOKEN:
        print("GITHUB_TOKEN not set, skipping report trigger")
        return False

    url = f"https://api.github.com/repos/{GITHUB_REPO}/actions/workflows/daily-reports.yml/dispatches"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }
    payload = {
        "ref": "main",
        "inputs": {
            "subscriber_id": subscriber_id,
        },
    }

    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        if resp.status_code == 204:
            print(f"Triggered report workflow for subscriber {subscriber_id}")
            return True
        else:
            print(f"GitHub dispatch error: {resp.status_code} {resp.text}")
            return False
    except Exception as e:
        print(f"GitHub dispatch error: {e}")
        return False


# ── Conversation management ──

def get_conversation(phone):
    """Get or create a conversation for a phone number."""
    now = time.time()

    if phone in conversations:
        conv = conversations[phone]
        if now - conv["last_active"] < CONVERSATION_TTL:
            conv["last_active"] = now
            return conv
        else:
            del conversations[phone]

    conv = {
        "history": [],
        "last_active": now,
        "pending_data": {},
    }
    conversations[phone] = conv
    return conv


def add_to_history(conv, role, content):
    """Add a message to conversation history, keeping it bounded."""
    # For Claude, we store the raw text (not the JSON response)
    conv["history"].append({"role": role, "content": content})
    # Keep last 20 messages to stay within context limits
    if len(conv["history"]) > 20:
        conv["history"] = conv["history"][-20:]


# ── Message handling ──

def handle_message(phone, text):
    """Process an incoming WhatsApp message and return a reply."""
    conv = get_conversation(phone)

    # Look up existing kids linked to this phone number
    if "known_kids" not in conv:
        kids = lookup_by_phone(phone)
        conv["known_kids"] = kids
        if kids:
            conv["pending_data"]["email"] = kids[0]["email"]

    # Build context about known kids for Claude (inject on first message only)
    known_kids_context = ""
    if conv.get("known_kids") and len(conv["history"]) == 0:
        kids_list = ", ".join(k["name"] for k in conv["known_kids"])
        email = conv["known_kids"][0]["email"]
        known_kids_context = (
            f"\n[SYSTEM: This parent's phone is linked to these existing reports: "
            f"{kids_list} (email: {email}). You do NOT need to ask for their email. "
            f"For updates, you already know which kids they have.]"
        )

    msg_for_claude = text + known_kids_context
    add_to_history(conv, "user", msg_for_claude)

    # Parse with Claude (full conversation history gives it context for multi-step flow)
    result = parse_message(msg_for_claude, conv["history"][:-1])
    reply = result["reply"]
    action = result.get("action")
    data = result.get("data")
    needs = result.get("needs")

    # Track what Claude says is still needed
    if needs:
        conv["pending_needs"] = needs

    # Accumulate partial data across messages so nothing gets lost
    if data:
        pending = conv.get("pending_data", {})
        for key, val in data.items():
            if val is not None:
                pending[key] = val
        conv["pending_data"] = pending

    # Store Claude's reply in history
    add_to_history(conv, "assistant", reply)

    # ── Execute actions ──

    if action == "create":
        # Merge accumulated data with final data
        final_data = conv.get("pending_data", {})
        if data:
            final_data.update(data)

        if not final_data.get("name") or not final_data.get("email"):
            return reply

        sub = create_subscriber(final_data, phone=phone)
        if sub:
            conv["known_kids"].append(sub)
            sub_id = sub.get("id", "")
            manage_url = f"{SETTINGS_URL}?id={sub_id}"
            reply += f"\n\n📎 If you'd like to review your selections, reorder sections, or make changes, use this link anytime: {manage_url}"
            # Trigger immediate first report
            if sub_id:
                trigger_report_for_subscriber(sub_id)
            # Clear pending data after successful creation
            conv["pending_data"] = {}
            conv["pending_needs"] = []
        else:
            reply = "Hmm, something went wrong saving that. Could you try again?"

    elif action == "update" and data:
        email = data.get("email") or conv.get("pending_data", {}).get("email")
        subs = conv.get("known_kids") or (lookup_subscribers(email) if email else [])
        if subs:
            name_raw = data.get("name") or conv.get("pending_data", {}).get("name") or ""
            name_match = name_raw.lower().rstrip("'s").rstrip("'s")
            target = None

            # Exact match first
            for s in subs:
                if name_match and s["name"].lower() == name_match:
                    target = s
                    break

            # Partial/contains match as fallback
            if not target and name_match:
                for s in subs:
                    if name_match in s["name"].lower() or s["name"].lower() in name_match:
                        target = s
                        break

            # Single subscriber — no ambiguity
            if not target and len(subs) == 1:
                target = subs[0]

            if target:
                conv["pending_data"]["name"] = target["name"]
                update_fields = {k: v for k, v in data.items()
                                 if k not in ("email", "name", "id")}
                if update_fields:
                    update_subscriber(target["id"], update_fields)
        else:
            reply = "I couldn't find an active report linked to this number. What email is the report under?"

    elif action == "unsubscribe" and data:
        email = data.get("email")
        name = data.get("name")
        if deactivate_subscriber(email=email, name=name):
            pass
        else:
            reply = "I couldn't find that subscription. It may already be inactive."

    elif action == "lookup" and data:
        email = data.get("email")
        if email:
            subs = lookup_subscribers(email)
            if subs:
                links = "\n".join(
                    f"• {s['name']}: {SETTINGS_URL}?id={s['id']}"
                    for s in subs
                )
                reply += f"\n\n{links}"
            else:
                reply = "No active reports found for that email."

    elif action == "feature_request" and data:
        feature = data.get("request", "unknown")
        if ADMIN_PHONE:
            kids = conv.get("known_kids", [])
            if kids:
                names = ", ".join(k["name"] for k in kids)
                email = kids[0].get("email", "unknown")
                who = f"{names} ({email})"
            else:
                who = f"phone {phone}"
            notify = f"💡 Feature request from {who}:\n\"{feature}\""
            send_whatsapp_message(ADMIN_PHONE, notify)

    return reply


# ── Flask routes ──

@app.route("/webhook", methods=["GET"])
def verify():
    """Handle the Meta webhook verification challenge."""
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("Webhook verified!")
        return challenge, 200
    return "Forbidden", 403


@app.route("/webhook", methods=["POST"])
def webhook():
    """Handle incoming WhatsApp messages."""
    body = request.get_json()

    if not body:
        return "OK", 200

    try:
        for entry in body.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                messages = value.get("messages", [])

                for msg in messages:
                    if msg.get("type") != "text":
                        continue

                    msg_id = msg.get("id", "")
                    if msg_id:
                        now = time.time()
                        if msg_id in processed_messages and now - processed_messages[msg_id] < DEDUP_TTL:
                            print(f"[dedup] Skipping duplicate message {msg_id}")
                            continue
                        processed_messages[msg_id] = now
                        # Clean old entries
                        for k in list(processed_messages):
                            if now - processed_messages[k] > DEDUP_TTL:
                                del processed_messages[k]

                    phone = msg["from"]
                    text = msg["text"]["body"]
                    print(f"[{phone}] {text}")

                    reply = handle_message(phone, text)
                    send_whatsapp_message(phone, reply)

    except Exception as e:
        print(f"Webhook error: {e}")
        import traceback
        traceback.print_exc()

    return "OK", 200


@app.route("/trigger-report", methods=["POST", "OPTIONS"])
def trigger_report():
    """Trigger an immediate report for a newly signed-up subscriber."""
    if request.method == "OPTIONS":
        resp = jsonify({"ok": True})
        resp.headers["Access-Control-Allow-Origin"] = "*"
        resp.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return resp, 200

    data = request.get_json()
    sub_id = data.get("subscriber_id") if data else None
    if not sub_id:
        resp = jsonify({"error": "subscriber_id required"})
        resp.headers["Access-Control-Allow-Origin"] = "*"
        return resp, 400

    ok = trigger_report_for_subscriber(sub_id)
    resp = jsonify({"triggered": ok})
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp, 200 if ok else 500


@app.route("/", methods=["GET", "HEAD"])
@app.route("/health", methods=["GET", "HEAD"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "service": "mysportsreport-whatsapp-bot"}), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
