"""
Claude-powered natural language parser for WhatsApp messages.
Converts casual text into structured subscriber configs or edit commands.
"""

import json
import os
import anthropic

from config import (
    NBA_TEAMS, NBA_SECTIONS, NBA_SECTION_LABELS,
    SOCCER_LEAGUES, SOCCER_SECTIONS, SOCCER_SECTION_LABELS,
    MLS_TEAMS, MLS_SECTIONS, COLOR_THEMES,
    DEFAULT_NBA_SECTIONS, DEFAULT_NBA_SECTIONS_WITH_TEAM,
    DEFAULT_SOCCER_SECTIONS, DEFAULT_MLS_SECTIONS,
)

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))

SYSTEM_PROMPT = f"""You are a helpful assistant for "My Sports Report," a service that sends kids personalized daily printable sports reports. You help parents sign up their kids and manage their report preferences via WhatsApp.

## Your Capabilities
- Sign up new subscribers (create a new report)
- Edit existing subscriber preferences (add/remove sports, teams, sections)
- Answer questions about the service
- Help with unsubscribing

## Available Sports & Options

### NBA
Teams: {json.dumps(NBA_TEAMS)}
Sections: {json.dumps(NBA_SECTION_LABELS)}
If a team is selected, include "team_focus" by default.

### European Soccer
Leagues: {json.dumps(SOCCER_LEAGUES)}
Sections: {json.dumps(SOCCER_SECTION_LABELS)}

### MLS
Teams: {json.dumps(MLS_TEAMS)}
Sections: results, team_focus

### Color Themes
Available: {json.dumps(COLOR_THEMES)}

## Response Format

CRITICAL: Your entire response must be ONLY a single JSON object. No text before or after the JSON. No markdown code blocks. Just the raw JSON object.

{{
  "reply": "Your friendly WhatsApp message to the user",
  "action": null | "create" | "update" | "unsubscribe" | "lookup",
  "data": null | {{...subscriber config...}},
  "needs": null | ["name", "email", "sports"]
}}

### Actions:
- **null**: Just chatting, answering questions, or need more info
- **"create"**: Create a new subscriber. "data" must have: name, email, sports array
- **"update"**: Update an existing subscriber. "data" has the fields to change
- **"unsubscribe"**: Deactivate a subscriber. "data" must have "email" or "name"
- **"lookup"**: Look up existing subscriber(s) by email

### The "needs" field:
When you have a partial signup (e.g., they gave a name and sport but no email), set "needs" to the list of missing required fields so the system knows what to ask next.

### Subscriber data format (for create):
{{
  "name": "Kid's first name",
  "email": "parent@email.com",
  "color_theme": "blue",
  "favorite_athlete": "Shai Gilgeous-Alexander",
  "sports": [
    {{
      "sport": "nba",
      "order": 1,
      "favorite_team": "Oklahoma City Thunder",
      "sections": ["scores", "team_focus", "top_scorers", "standings", "todays_games"]
    }},
    {{
      "sport": "soccer",
      "order": 2,
      "leagues": ["Premier League", "La Liga"],
      "sections": ["results", "standings"],
      "options": {{"show_scorers": true}}
    }}
  ]
}}

## Guidelines
- Be friendly, concise, and use casual language appropriate for WhatsApp
- Use emojis sparingly but naturally (🏀 ⚽ 📊)
- When someone wants to sign up, gather: kid's name, parent's email, which sports, and optionally favorite team(s) and athlete
- You can gather info across multiple messages — don't force everything at once
- If they say something like "my son loves the Lakers," infer NBA + Lakers as favorite team
- Use sensible defaults for sections — most people want everything
- Keep replies SHORT — this is WhatsApp, not email
- For team names, always use the official full name in the data (e.g., "Los Angeles Lakers" not just "Lakers")
- If someone mentions a sport you don't support yet, let them know what's available
- favorite_athlete is optional — only include if they mention a favorite player
"""


def parse_message(user_message, conversation_history=None):
    """
    Parse a WhatsApp message using Claude.

    Args:
        user_message: The text the user sent
        conversation_history: List of prior messages in the conversation
            [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]

    Returns:
        dict with keys: reply, action, data, needs
    """
    messages = []

    if conversation_history:
        for msg in conversation_history:
            messages.append(msg)

    messages.append({"role": "user", "content": user_message})

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=messages,
        )

        raw = response.content[0].text.strip()

        # Extract JSON from the response
        json_str = None

        # Try markdown code blocks first
        if "```json" in raw:
            json_str = raw.split("```json")[1].split("```")[0].strip()
        elif "```" in raw:
            json_str = raw.split("```")[1].split("```")[0].strip()
        else:
            # Find the outermost JSON object by matching braces
            start = raw.find("{")
            if start != -1:
                depth = 0
                for i in range(start, len(raw)):
                    if raw[i] == "{":
                        depth += 1
                    elif raw[i] == "}":
                        depth -= 1
                        if depth == 0:
                            json_str = raw[start:i + 1]
                            break

        if not json_str:
            json_str = raw

        result = json.loads(json_str)

        # Validate required fields
        if "reply" not in result:
            result["reply"] = "Something went wrong — could you try again?"
        if "action" not in result:
            result["action"] = None
        if "data" not in result:
            result["data"] = None
        if "needs" not in result:
            result["needs"] = None

        return result

    except json.JSONDecodeError:
        # If JSON parsing fails entirely, use the raw text but strip any JSON-looking content
        clean = raw
        start = raw.find("{")
        if start > 0:
            clean = raw[:start].strip()
        return {
            "reply": clean if clean else "I didn't quite get that. Could you try again?",
            "action": None,
            "data": None,
            "needs": None,
        }
    except Exception as e:
        print(f"Claude API error: {e}")
        return {
            "reply": "Sorry, I'm having a moment. Try again in a sec! 🙏",
            "action": None,
            "data": None,
            "needs": None,
        }
