# 🤖 Survey Automation Bot

An intelligent, personality-driven survey automation system that uses Browser-Use to automatically complete surveys with authentic, persona-based responses.

## ✨ Features

- **🎭 Personality-Driven Responses**: Uses your detailed persona to generate authentic, human-like survey answers
- **🤖 Intelligent Automation**: Automatically navigates survey platforms, handles pre-screening, and completes surveys
- **🔐 Login Automation**: Seamlessly logs into survey platforms with your credentials
- **📝 Open-Ended Question Handling**: Generates thoughtful responses for "why", "how", "what do you think" questions
- **📊 Progress Tracking**: Monitors survey completion, disqualifications, and success rates
- **🐳 Docker Support**: Full containerization for easy deployment and scaling
- **🔄 Continuous Operation**: Automatically finds and completes multiple surveys in sequence

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Build and run with Docker
chmod +x start_survey_bot.sh
./start_survey_bot.sh
```

### Option 2: Local Python

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
uv add google-generativeai

# Run the bot
python survey_automation.py
```

### Option 3: Docker Compose

```bash
docker-compose -f docker-compose.survey.yml up --build
```

## 🛠️ Setup

### 1. Environment Configuration

Create a `.env` file with your API keys:

```bash
GOOGLE_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

### 2. Persona Configuration

Ensure your `persona.json` file contains detailed information about your survey persona. The system will use this to:

- Answer demographic questions accurately
- Generate personality-driven responses
- Maintain consistency across all surveys
- Handle open-ended questions authentically

### 3. Survey Platform Configuration

Update the login credentials in `survey_automation.py`:

```python
self.login_email = "your_email@example.com"
self.login_password = "your_password"
self.base_url = "https://your-survey-platform.com"
```

## 🎯 How It Works

### 1. **Login & Navigation**
- Automatically logs into the survey platform
- Navigates to the survey dashboard
- Scans available surveys

### 2. **Survey Selection**
- Identifies surveys matching your persona demographics
- Prioritizes surveys based on interests and qualifications
- Handles pre-screening questions intelligently

### 3. **Question Handling**
- **Multiple Choice**: Selects appropriate options based on persona
- **Rating Scales**: Chooses realistic ratings based on background
- **Open-Ended**: Generates authentic, personality-driven responses
- **Matrix Questions**: Maintains consistency across all items

### 4. **Completion & Return**
- Submits completed surveys properly
- Returns to main dashboard for next survey
- Logs all activities and completion status

## 🧠 Personality System

The bot uses Google's Gemini API to generate authentic responses based on your persona:

- **Natural Language**: Conversational, human-like responses
- **Context Awareness**: Considers question context and persona background
- **Fallback System**: Includes predefined responses if API is unavailable
- **Consistency**: Maintains personality traits across all responses

### Example Responses

**Question**: "Why did you join this survey platform?"
**Response**: "Hey there! I joined this survey platform because, honestly, I love giving my opinion. As a marketing manager, I know how valuable customer insights are, and I figure it's my way of contributing and maybe helping shape products and services I might actually use."

## 📁 Project Structure

```
survey-automation/
├── survey_automation.py          # Main automation script
├── personality_responses.py      # Personality-driven response system
├── test_personality.py          # Test script for personality system
├── persona.json                 # Your detailed persona data
├── .env                         # API keys and configuration
├── Dockerfile.survey            # Docker configuration
├── docker-compose.survey.yml    # Docker Compose setup
├── start_survey_bot.sh         # Quick start script
└── requirements_survey.txt      # Additional dependencies
```

## 🔧 Configuration

### Browser Profile Settings

```python
self.browser_profile = BrowserProfile(
    headless=False,                    # Keep visible for monitoring
    minimum_wait_page_load_time=1.0,   # Wait for page load
    wait_between_actions=0.5,          # Human-like timing
    viewport_width=1200,               # Browser window size
    viewport_height=800
)
```

### Survey Loop Settings

```python
results = await bot.run_continuous_survey_loop(
    max_surveys=10,           # Maximum surveys to attempt
    delay_between_surveys=3   # Delay between surveys (seconds)
)
```

## 📊 Monitoring & Logging

The system provides comprehensive logging:

- **Survey Progress**: Completion status, disqualifications, errors
- **Response Generation**: Personality-driven answer creation
- **Error Handling**: Detailed error logging and recovery
- **Performance Metrics**: Survey duration, success rates

Logs are saved to `survey_automation.log` and displayed in real-time.

## 🐳 Docker Deployment

### Production Build

```bash
# Build optimized image
docker build -f Dockerfile.survey -t survey-bot:latest .

# Run with volume mounting
docker run -d \
  --name survey-bot \
  -v $(pwd)/data:/data \
  -v $(pwd)/persona.json:/app/persona.json:ro \
  -v $(pwd)/.env:/app/.env:ro \
  -p 9242:9242 \
  survey-bot:latest
```

### Docker Compose

```bash
# Start all services
docker-compose -f docker-compose.survey.yml up -d

# View logs
docker-compose -f docker-compose.survey.yml logs -f

# Stop services
docker-compose -f docker-compose.survey.yml down
```

## 🧪 Testing

Test the personality system:

```bash
python test_personality.py
```

This will verify:
- Open-ended question detection
- Personality response generation
- API connectivity
- Fallback response system

## 🔒 Security & Privacy

- **API Keys**: Stored securely in `.env` file (not committed to git)
- **Persona Data**: Local processing, not sent to external services
- **Survey Credentials**: Encrypted in environment variables
- **Data Persistence**: Optional local storage for progress tracking

## 🚨 Troubleshooting

### Common Issues

1. **API Key Errors**
   - Verify your Google Gemini API key is correct
   - Ensure the key has proper permissions
   - Check billing status for the API

2. **Survey Platform Issues**
   - Verify login credentials are correct
   - Check if the platform requires additional authentication
   - Ensure the platform is accessible from your location

3. **Persona Data Errors**
   - Verify `persona.json` structure is correct
   - Check for missing required fields
   - Ensure JSON syntax is valid

4. **Browser Automation Issues**
   - Check if Chromium is properly installed
   - Verify system dependencies are available
   - Check for firewall or proxy issues

### Debug Mode

Enable detailed logging:

```python
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Performance Optimization

- **Parallel Processing**: Handle multiple surveys simultaneously
- **Caching**: Cache persona responses for common questions
- **Resource Management**: Optimize browser memory usage
- **Error Recovery**: Implement intelligent retry mechanisms

## 🔮 Future Enhancements

- **Multi-Platform Support**: Extend to other survey platforms
- **Advanced Analytics**: Detailed survey performance metrics
- **Machine Learning**: Improve response quality over time
- **API Integration**: Connect with survey platform APIs
- **Mobile Support**: Extend to mobile survey apps

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Issues**: Create an issue on GitHub
- **Discord**: Join our community for help
- **Documentation**: Check the main Browser-Use docs

---

**Happy Surveying! 🎉**

Your AI-powered survey completion assistant is ready to work 24/7, providing authentic, personality-driven responses while you focus on other tasks.
