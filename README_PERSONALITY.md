# Personality-Driven Survey Bot

This enhancement adds natural, personality-driven responses to open-ended survey questions using the Google Gemini API.

## Features

- **Natural Language Responses**: Generates conversational, authentic responses based on your persona
- **Personality Consistency**: Maintains consistent personality traits across all responses
- **Fallback System**: Includes fallback responses when API is unavailable
- **Context Awareness**: Considers question context and persona background

## Setup

### 1. Get Google Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the API key

### 2. Configure Environment

1. Edit the `.env` file:
```bash
GOOGLE_API_KEY=your_actual_api_key_here
```

2. Install dependencies (if not already installed):
```bash
source venv/bin/activate
pip install google-generativeai python-dotenv
```

### 3. Test the System

Run the test script to verify everything works:
```bash
python test_personality.py
```

## How It Works

### Personality Generation

The system creates a comprehensive personality profile from your `persona.json` data:

- **Core Traits**: Age, gender, location, job, marital status
- **Lifestyle**: Hobbies, sports, gaming habits, reading preferences
- **Technology**: Device ownership, early adopter status, brand preferences
- **Communication Style**: Conversational, natural language, authentic opinions

### Response Generation

When the bot encounters an open-ended question:

1. **Detection**: Identifies questions containing words like "why", "how", "what", "tell", "describe", "explain"
2. **Context Analysis**: Extracts question context from the DOM
3. **Personality Response**: Generates a natural response using Gemini API
4. **Fallback**: Uses predefined responses if API fails

### Example Responses

**Question**: "Why did you join Qmee?"
**Response**: "I joined Qmee because I'm always looking for ways to earn a little extra money, especially since I work in tech and spend a lot of time online anyway. Plus, I like trying out new apps and services."

**Question**: "What do you think about technology?"
**Response**: "I'm definitely a tech person - I work in IT and I'm usually one of the first to try new gadgets and apps. I love how technology makes life easier."

## Configuration

### Customizing Personality

Edit `persona.json` to modify personality traits:

```json
{
  "about_you": {
    "full_name": "Your Name",
    "age": 30,
    "city": "Your City",
    "state": "Your State"
  },
  "work": {
    "job_title": "Your Job Title",
    "company_industry": "Your Industry"
  },
  "leisure": {
    "hobbies_and_interests": ["Your", "Hobbies", "Here"]
  }
}
```

### Adjusting Response Style

Modify the personality prompt in `personality_responses.py`:

```python
COMMUNICATION_STYLE = """
- Be conversational and natural
- Use contractions (I'm, you're, don't)
- Show personality and opinions
- Be honest about likes/dislikes
"""
```

## Integration with Bot

The personality system is automatically integrated into the main bot:

1. **Import**: `from personality_responses import generate_personality_response`
2. **Detection**: Automatically detects open-ended questions
3. **Generation**: Creates personality-driven responses
4. **Fallback**: Uses original text if generation fails

## Troubleshooting

### API Key Issues

If you get "API key not valid" errors:
1. Verify your API key in `.env`
2. Check that the key is active in Google AI Studio
3. Ensure you have billing set up for the Gemini API

### Response Quality

If responses seem generic:
1. Check your `persona.json` has detailed information
2. Verify the personality prompt includes relevant traits
3. Test with the `test_personality.py` script

### Performance Issues

If responses are slow:
1. The system includes fallback responses for reliability
2. API calls are cached to improve performance
3. Consider adjusting the `max_output_tokens` parameter

## Advanced Usage

### Custom Response Templates

Add custom response patterns in `personality_responses.py`:

```python
def _generate_fallback_response(self, question):
    if "technology" in question.lower():
        return "I'm a tech enthusiast who loves trying new gadgets..."
    elif "family" in question.lower():
        return "Family is really important to me..."
```

### Context Enhancement

Add more context to responses:

```python
context = f"Current page: {page_title}, Previous answers: {previous_answers}"
response = await generate_personality_response(question, persona_data, context)
```

## Security Notes

- API keys are stored in `.env` file (not committed to git)
- Responses are generated locally, not stored
- No personal data is sent to external services beyond the API call

## Support

If you encounter issues:
1. Check the console output for error messages
2. Verify your API key is correct
3. Test with the provided test script
4. Check that all dependencies are installed 