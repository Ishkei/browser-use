#!/usr/bin/env python3
"""
Improved Survey Automation Bot for TopSurveys
Optimized for better navigation and survey completion
"""

import asyncio
import json
import logging
import os
import sys
from typing import Dict, Any, List, Optional
from datetime import datetime
import time

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
from browser_use import Agent, ChatGoogle, BrowserProfile
from personality_responses import generate_personality_response

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('survey_automation_improved.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ImprovedSurveyBot:
    def __init__(self):
        """Initialize the improved survey automation bot."""
        self.login_email = "marerise28@gmail.com"
        self.login_password = "iinqxnE%kuA#!Evubr3q%"
        self.base_url = "https://app.topsurveys.app/Surveys"
        self.login_url = "https://app.topsurveys.app/app-login"
        self.dashboard_url = "https://app.topsurveys.app/dashboard"

        # Initialize Gemini LLM
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")

        self.llm = ChatGoogle(
            model='gemini-2.0-flash-exp',
            api_key=api_key,
            temperature=0.1
        )

        # ChromeOS-optimized browser profile with better settings
        self.browser_profile = BrowserProfile(
            headless=True,  # Use headless for stability
            minimum_wait_page_load_time=3.0,  # Longer wait for TopSurveys
            wait_between_actions=2.0,  # Slower for reliability
            viewport_width=1366,  # Standard desktop width
            viewport_height=768,
            # Enhanced ChromeOS browser arguments
            args=[
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--disable-software-rasterizer',
                '--disable-background-timer-throttling',
                '--disable-backgrounding-occluded-windows',
                '--disable-renderer-backgrounding',
                '--disable-features=TranslateUI',
                '--disable-ipc-flooding-protection',
                '--disable-popup-blocking',
                '--disable-default-apps',
                '--no-first-run',
                '--disable-extensions',
                '--disable-web-security',  # Sometimes needed for survey sites
                '--disable-features=VizDisplayCompositor',
                '--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            ]
        )

        # Load persona data
        self.persona_data = self._load_persona_data()

        # Survey tracking
        self.completed_surveys = []
        self.failed_surveys = []
        self.login_attempts = 0
        self.max_login_attempts = 3

        logger.info("Improved survey automation bot initialized for TopSurveys")

    def _load_persona_data(self) -> Dict[str, Any]:
        """Load persona data for intelligent survey responses."""
        try:
            with open('persona.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load persona data: {e}")
            raise

    def _create_precise_login_task(self) -> str:
        """Create a very specific task for TopSurveys TWO-STEP login."""
        return f"""
You are a precise survey platform automation assistant. Your task is to log into TopSurveys using their TWO-STEP login process.

TOPSURVEYS TWO-STEP LOGIN WORKFLOW:
1. **Navigate to Login Page**: Go to https://app.topsurveys.app/app-login
2. **Wait for Page Load**: Wait at least 5 seconds for the page to fully load
3. **Handle Language Popup**: If you see a language/country selection popup, close it or select English
4. **STEP 1 - Email Entry**:
   - Find the email input field (usually with placeholder "Email")
   - Enter email: "{self.login_email}"
   - Find and click the "Continue" button (NOT the login button yet)
5. **Wait for Password Form**: Wait for the page to load and show the password field
6. **STEP 2 - Password Entry**:
   - Find the password input field (type="password")
   - Enter password: "{self.login_password}"
   - Find and click the "Log in" button
7. **Verify Login**: Check if you are redirected to dashboard or survey page

CRITICAL INSTRUCTIONS:
- This is a TWO-STEP process: Email → Continue → Password → Log in
- Do NOT click login button after entering email
- Click "Continue" button after email entry
- Wait for password field to appear
- Then enter password and click "Log in" button
- Look for buttons by exact text: "Continue" and "Log in"

IMPORTANT:
- Be very patient and wait for elements to appear
- Use the exact URLs provided
- Don't try to navigate away until login is confirmed
- If login fails, try again with different element selectors
- Look for elements by their text content, not just index

SUCCESS CRITERIA:
- Successfully completed both login steps
- Redirected to dashboard or survey page
- No longer on login page
"""

    def _create_survey_discovery_task(self) -> str:
        """Create a task for finding and starting surveys."""
        return f"""
You are now logged into TopSurveys. Your task is to find and start available surveys.

SURVEY DISCOVERY STRATEGY:
1. **Check Current Page**: Are you on a dashboard or survey listing page?
2. **Look for Survey Cards**: Search for elements containing survey titles, descriptions, or "Start Survey" buttons
3. **Scan for Links**: Look for links or buttons that say "Take Survey", "Start", "Begin", or survey titles
4. **Filter by Demographics**: Prioritize surveys that match:
   - Age: {self.persona_data['about_you']['age']}
   - Gender: {self.persona_data['about_you']['gender']}
   - Location: {self.persona_data['about_you']['city']}, {self.persona_data['about_you']['state']}
   - Occupation: {self.persona_data['about_you']['occupation']}
   - Income: {self.persona_data['family_and_household']['combined_household_income']}

5. **Click Survey**: Click on the first qualifying survey you find
6. **Handle Popups**: Close any language/country selection popups that appear

SUCCESS CRITERIA:
- Found at least one available survey
- Clicked to start a survey
- Now on a survey page (not dashboard)
"""

    def _create_survey_completion_task(self) -> str:
        """Create a task for completing surveys with personality."""
        return f"""
You are now on a survey page. Complete the survey using your persona information.

SURVEY COMPLETION RULES:
1. **Answer Demographics**: Use your persona data for all demographic questions:
   - Age: {self.persona_data['about_you']['age']}
   - Gender: {self.persona_data['about_you']['gender']}
   - Location: {self.persona_data['about_you']['city']}, {self.persona_data['about_you']['state']}
   - Occupation: {self.persona_data['about_you']['occupation']}
   - Income: {self.persona_data['family_and_household']['combined_household_income']}
   - Education: {self.persona_data['about_you']['education']}
   - Marital Status: {self.persona_data['about_you']['marital_status']}
   - Children: {self.persona_data['family_and_household']['children']}

2. **Handle Open-Ended Questions**: For questions containing words like "why", "how", "describe", "explain", "tell me":
   - Generate natural, personality-driven responses
   - Keep responses 2-4 sentences, conversational
   - Reference your background as Jordan Mitchell appropriately

3. **Rating Scales**: Choose ratings that match your persona's lifestyle and preferences
4. **Multiple Choice**: Select options that align with your demographics and interests
5. **Progress Through Survey**: Click "Next", "Continue", or "Submit" buttons to advance

6. **Quality Assurance**:
   - Answer thoughtfully and realistically
   - Don't rush through questions
   - Maintain consistency with your persona
   - If you don't qualify, acknowledge it gracefully

SUCCESS CRITERIA:
- Complete the entire survey
- Submit successfully
- Return to survey dashboard
"""

    async def perform_login(self) -> bool:
        """Perform login to TopSurveys with improved error handling."""
        logger.info("Starting improved login process...")

        try:
            # Create login agent with specific instructions
            agent = Agent(
                task=self._create_precise_login_task(),
                llm=self.llm,
                browser_profile=self.browser_profile,
                max_actions_per_step=1,
                use_vision=True,
                save_screenshots=False,
                extend_system_message="Focus on TopSurveys TWO-STEP login: Email → Continue → Password → Log in. Be precise with element identification and patient waiting. Use text content and attributes to find elements, not just indices.",
            )

            # Run login
            start_time = time.time()
            history = await agent.run(max_steps=25)  # More steps for login
            end_time = time.time()

            # Check if login was successful
            final_url = history.final_result.url if hasattr(history, 'final_result') else ""

            if any(keyword in final_url.lower() for keyword in ['dashboard', 'survey', 'app.topsurveys.app']):
                if 'login' not in final_url.lower():
                    logger.info("✅ Login successful!")
                    return True
                else:
                    logger.warning("⚠️ Still on login page, may need retry")
                    return False
            else:
                logger.warning(f"⚠️ Unexpected URL after login: {final_url}")
                return False

        except Exception as e:
            logger.error(f"Login failed: {e}")
            return False

    async def discover_and_start_survey(self) -> bool:
        """Find and start an available survey."""
        logger.info("Starting survey discovery...")

        try:
            # Create survey discovery agent
            agent = Agent(
                task=self._create_survey_discovery_task(),
                llm=self.llm,
                browser_profile=self.browser_profile,
                max_actions_per_step=1,
                use_vision=True,
                save_screenshots=False,
                extend_system_message="Look for survey cards, buttons, and links. Be thorough in scanning the page for survey opportunities.",
            )

            # Run survey discovery
            history = await agent.run(max_steps=30)

            # Check if we found and started a survey
            final_url = history.final_result.url if hasattr(history, 'final_result') else ""

            # Look for survey-related URLs or content
            survey_indicators = ['survey', 'question', 'quiz', 'poll', 'form']
            if any(indicator in final_url.lower() for indicator in survey_indicators):
                logger.info("✅ Found and started a survey!")
                return True
            else:
                logger.warning(f"⚠️ No survey found or started. Current URL: {final_url}")
                return False

        except Exception as e:
            logger.error(f"Survey discovery failed: {e}")
            return False

    async def complete_single_survey(self) -> Dict[str, Any]:
        """Complete a single survey with improved handling."""
        logger.info("Starting survey completion...")

        try:
            # Create survey completion agent
            agent = Agent(
                task=self._create_survey_completion_task(),
                llm=self.llm,
                browser_profile=self.browser_profile,
                max_actions_per_step=1,
                use_vision=True,
                save_screenshots=False,
                extend_system_message="Complete the survey systematically. Answer all questions based on persona data. Handle open-ended questions with personality.",
            )

            # Run survey completion
            start_time = time.time()
            history = await agent.run(max_steps=100)  # More steps for surveys
            end_time = time.time()

            # Analyze completion
            result = {
                'status': 'completed',
                'duration': round(end_time - start_time, 2),
                'steps_taken': len(history.action_results) if hasattr(history, 'action_results') else 0,
                'timestamp': datetime.now().isoformat(),
                'completion_method': 'improved_agent'
            }

            # Check completion status
            final_url = history.final_result.url if hasattr(history, 'final_result') else ""

            if "qualify" in final_url.lower() or "disqualified" in final_url.lower():
                result['status'] = 'disqualified'
                logger.info("❌ Disqualified from survey")
            elif any(keyword in final_url.lower() for keyword in ['dashboard', 'surveys', 'complete']):
                result['status'] = 'completed'
                logger.info("✅ Survey completed successfully!")
            else:
                result['status'] = 'unknown'
                logger.warning(f"⚠️ Unknown completion status: {final_url}")

            return result

        except Exception as e:
            logger.error(f"Survey completion failed: {e}")
            return {
                'status': 'failed',
                'error': str(e),
                'timestamp': datetime.now().isoformat(),
                'completion_method': 'improved_agent'
            }

    async def run_improved_survey_session(self, max_surveys: int = 3) -> Dict[str, Any]:
        """Run an improved survey session with better error handling."""
        logger.info("Starting improved survey session...")

        session_start = datetime.now()
        completed_count = 0
        disqualified_count = 0
        failed_count = 0

        try:
            # Step 1: Login
            login_success = await self.perform_login()

            if not login_success:
                logger.error("❌ Login failed, cannot proceed")
                return {
                    'error': 'Login failed',
                    'completed': 0,
                    'disqualified': 0,
                    'failed': 0,
                    'session_duration': (datetime.now() - session_start).total_seconds()
                }

            # Step 2: Complete surveys
            for i in range(max_surveys):
                logger.info(f"=== Improved Survey {i+1}/{max_surveys} ===")

                # Find and start a survey
                survey_found = await self.discover_and_start_survey()

                if not survey_found:
                    logger.warning("No survey found, trying again...")
                    await asyncio.sleep(5)  # Wait before retry
                    continue

                # Complete the survey
                result = await self.complete_single_survey()

                # Track results
                if result['status'] == 'completed':
                    completed_count += 1
                    self.completed_surveys.append(result)
                elif result['status'] == 'disqualified':
                    disqualified_count += 1
                else:
                    failed_count += 1
                    self.failed_surveys.append(result)

                logger.info(f"Progress: {completed_count} completed, {disqualified_count} disqualified, {failed_count} failed")

                # Wait between surveys
                if i < max_surveys - 1:
                    logger.info("Waiting 10 seconds before next survey...")
                    await asyncio.sleep(10)

            # Session summary
            session_duration = (datetime.now() - session_start).total_seconds()

            logger.info("=== Improved Session Complete ===")
            logger.info(f"Duration: {session_duration:.1f} seconds")
            logger.info(f"Completed: {completed_count}")
            logger.info(f"Disqualified: {disqualified_count}")
            logger.info(f"Failed: {failed_count}")

            return {
                'completed': completed_count,
                'disqualified': disqualified_count,
                'failed': failed_count,
                'session_duration': session_duration,
                'completed_surveys': self.completed_surveys,
                'failed_surveys': self.failed_surveys,
                'improvements_applied': [
                    'precise_login_flow',
                    'better_element_detection',
                    'improved_error_handling',
                    'survey_discovery_agent',
                    'persona_driven_completion'
                ]
            }

        except Exception as e:
            logger.error(f"Improved session failed: {e}")
            return {
                'error': str(e),
                'completed': completed_count,
                'disqualified': disqualified_count,
                'failed': failed_count,
                'session_duration': (datetime.now() - session_start).total_seconds()
            }

async def main():
    """Main function to run the improved survey automation."""
    print("🚀 Improved Survey Automation Bot for TopSurveys")
    print("=" * 55)

    # Initialize improved bot
    try:
        bot = ImprovedSurveyBot()
        print("✅ Improved bot initialized successfully")
        print("🎯 Optimized for TopSurveys platform")
        print("🧠 Using persona: Jordan Mitchell")
    except Exception as e:
        print(f"❌ Failed to initialize improved bot: {e}")
        return

    # Run improved session
    print("\n🎯 Starting improved survey session...")
    print("Improvements:")
    print("  ✅ Precise login flow with better element detection")
    print("  ✅ Dedicated survey discovery agent")
    print("  ✅ Improved error handling and recovery")
    print("  ✅ Persona-driven survey completion")
    print("  ✅ Better ChromeOS compatibility")

    results = await bot.run_improved_survey_session(max_surveys=3)

    # Print results
    print("\n📊 Improved Session Results:")
    print("=" * 35)
    print(f"✅ Surveys Completed: {results.get('completed', 0)}")
    print(f"❌ Surveys Disqualified: {results.get('disqualified', 0)}")
    print(f"⚠️  Surveys Failed: {results.get('failed', 0)}")

    if 'session_duration' in results:
        print(f"⏱️  Session Duration: {results['session_duration']:.1f} seconds")

    if results.get('improvements_applied'):
        print("🔧 Improvements Applied:")
        for improvement in results['improvements_applied']:
            print(f"   • {improvement}")

    if results.get('error'):
        print(f"💥 Error: {results['error']}")

    print("\n🎉 Improved survey automation complete!")

if __name__ == "__main__":
    asyncio.run(main())
