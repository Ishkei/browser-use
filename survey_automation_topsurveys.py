#!/usr/bin/env python3
"""
TopSurveys-Specific Survey Automation Bot
Highly optimized for TopSurveys platform workflow
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
        logging.FileHandler('survey_automation_topsurveys.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TopSurveysBot:
    def __init__(self):
        """Initialize the TopSurveys-specific bot."""
        self.login_email = "marerise28@gmail.com"
        self.login_password = "iinqxnE%kuA#!Evubr3q%"
        self.base_url = "https://app.topsurveys.app/Surveys"
        self.login_url = "https://app.topsurveys.app/app-login"

        # Initialize Gemini LLM
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")

        self.llm = ChatGoogle(
            model='gemini-2.0-flash-exp',
            api_key=api_key,
            temperature=0.1
        )

        # TopSurveys-optimized browser profile
        self.browser_profile = BrowserProfile(
            headless=True,  # Use headless for stability
            minimum_wait_page_load_time=2.0,  # Shorter for TopSurveys
            wait_between_actions=1.5,  # Moderate speed
            viewport_width=1280,  # Standard width
            viewport_height=720,
            # TopSurveys-specific browser arguments
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
                '--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            ]
        )

        # Load persona data
        self.persona_data = self._load_persona_data()

        # TopSurveys-specific tracking
        self.completed_surveys = []
        self.failed_surveys = []
        self.current_session = None

        logger.info("TopSurveys-specific automation bot initialized")

    def _load_persona_data(self) -> Dict[str, Any]:
        """Load persona data for intelligent survey responses."""
        try:
            with open('persona.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load persona data: {e}")
            raise

    def _create_topsurveys_login_task(self) -> str:
        """Create TopSurveys-specific login instructions."""
        return f"""
You are a specialized TopSurveys automation assistant. Your task is to log into TopSurveys using their specific TWO-STEP login workflow.

TOPSURVEYS TWO-STEP LOGIN WORKFLOW:
1. **Navigate to Login Page**: Go to https://app.topsurveys.app/app-login
2. **Handle Language Popup**: If a language/country selection appears, close it with 'X' or select English
3. **STEP 1 - Email Entry**: 
   - Find the email input field
   - Enter email: "{self.login_email}"
   - Click the "Continue" button (NOT login button yet)
4. **Wait for Password Form**: Wait for the page to load the password field
5. **STEP 2 - Password Entry**:
   - Find the password input field (type="password")
   - Enter password: "{self.login_password}"
   - Click the "Log in" button
6. **Verify Success**: Confirm you're redirected to dashboard or survey page

CRITICAL INSTRUCTIONS:
- This is a TWO-STEP process: Email → Continue → Password → Log in
- Do NOT click login button after entering email
- Click "Continue" button after email
- Wait for password field to appear
- Then enter password and click "Log in" button
- Look for buttons by exact text: "Continue" and "Log in"

SUCCESS INDICATORS:
- Successfully completed both steps
- Redirected away from login page
- Now on dashboard or survey listing page
"""

    def _create_survey_discovery_task(self) -> str:
        """Create TopSurveys-specific survey discovery."""
        return f"""
You are now on the TopSurveys dashboard. Your task is to find available surveys.

TOPSURVEYS DASHBOARD ANALYSIS:
1. **Scan for Survey Cards**: Look for survey listings with titles, descriptions, or earnings
2. **Find Action Buttons**: Search for "Take Survey", "Start", "Begin", or survey titles
3. **Check Availability**: Prioritize surveys that match:
   - Age: {self.persona_data['about_you']['age']}
   - Gender: {self.persona_data['about_you']['gender']}
   - Location: {self.persona_data['about_you']['city']}, {self.persona_data['about_you']['state']}
   - Occupation: {self.persona_data['about_you']['occupation']}

4. **Click to Start**: Click the first available qualifying survey
5. **Handle Confirmations**: Accept any survey start confirmations

SUCCESS INDICATORS:
- Now on a survey question page (not dashboard)
- Survey title or questions are visible
- Navigation shows survey progress
"""

    def _create_survey_completion_task(self) -> str:
        """Create TopSurveys-specific survey completion."""
        return f"""
You are now on a TopSurveys survey page. Complete the survey systematically.

TOPSURVEYS SURVEY COMPLETION:
1. **Answer Demographics**: Use exact persona data:
   - Age: {self.persona_data['about_you']['age']}
   - Gender: {self.persona_data['about_you']['gender']}
   - Location: {self.persona_data['about_you']['city']}, {self.persona_data['about_you']['state']}
   - Occupation: {self.persona_data['about_you']['occupation']}
   - Income: {self.persona_data['about_you']['combined_household_income']}
   - Education: {self.persona_data['about_you']['education']}
   - Marital Status: {self.persona_data['about_you']['marital_status']}

2. **Handle Question Types**:
   - **Multiple Choice**: Select options matching your persona
   - **Rating Scales**: Choose ratings based on lifestyle
   - **Open-Ended**: Generate authentic responses for "why", "how", "describe"
   - **Checkboxes**: Select all that apply to your situation

3. **Navigation**: Click "Next", "Continue", or "Submit" buttons
4. **Progress Tracking**: Monitor survey completion progress
5. **Final Submit**: Click final submission button when complete

QUALITY ASSURANCE:
- Answer all questions thoughtfully
- Maintain persona consistency
- Complete entire survey properly
- Return to dashboard when finished
"""

    async def perform_topsurveys_login(self) -> bool:
        """Perform TopSurveys login with specialized handling."""
        logger.info("Starting TopSurveys login process...")

        try:
            # Create TopSurveys-specific login agent
            agent = Agent(
                task=self._create_topsurveys_login_task(),
                llm=self.llm,
                browser_profile=self.browser_profile,
                max_actions_per_step=1,
                use_vision=True,
                save_screenshots=False,
                extend_system_message="Specialized for TopSurveys TWO-STEP login. First enter email and click Continue, then wait for password field and click Log in. Handle language popups and verify login success.",
            )

            # Run login with more time for TopSurveys
            start_time = time.time()
            history = await agent.run(max_steps=30)  # More steps for complex login
            end_time = time.time()

            # Check login result
            if hasattr(history, 'final_result') and history.final_result:
                result_text = history.final_result
                logger.info(f"Login result: {result_text}")

                # Look for success indicators
                success_indicators = [
                    'successfully logged in',
                    'login successful',
                    'dashboard',
                    'survey',
                    'welcome'
                ]

                if any(indicator in result_text.lower() for indicator in success_indicators):
                    logger.info("✅ TopSurveys login successful!")
                    return True
                else:
                    logger.warning(f"⚠️ Login result unclear: {result_text}")
                    return False
            else:
                logger.warning("⚠️ No login result available")
                return False

        except Exception as e:
            logger.error(f"TopSurveys login failed: {e}")
            return False

    async def discover_available_surveys(self) -> bool:
        """Find and start available TopSurveys surveys."""
        logger.info("Discovering available TopSurveys surveys...")

        try:
            # Create survey discovery agent
            agent = Agent(
                task=self._create_survey_discovery_task(),
                llm=self.llm,
                browser_profile=self.browser_profile,
                max_actions_per_step=1,
                use_vision=True,
                save_screenshots=False,
                extend_system_message="Scan TopSurveys dashboard for available surveys. Prioritize by demographic match.",
            )

            # Run survey discovery
            history = await agent.run(max_steps=25)

            # Check if survey was found and started
            if hasattr(history, 'final_result') and history.final_result:
                result_text = history.final_result
                logger.info(f"Survey discovery result: {result_text}")

                # Look for survey start indicators
                survey_indicators = [
                    'survey started',
                    'survey loaded',
                    'question',
                    'survey page',
                    'now on survey'
                ]

                if any(indicator in result_text.lower() for indicator in survey_indicators):
                    logger.info("✅ Survey found and started!")
                    return True
                else:
                    logger.warning(f"⚠️ No survey started: {result_text}")
                    return False
            else:
                logger.warning("⚠️ No survey discovery result")
                return False

        except Exception as e:
            logger.error(f"Survey discovery failed: {e}")
            return False

    async def complete_topsurveys_survey(self) -> Dict[str, Any]:
        """Complete a TopSurveys survey with specialized handling."""
        logger.info("Completing TopSurveys survey...")

        try:
            # Create survey completion agent
            agent = Agent(
                task=self._create_survey_completion_task(),
                llm=self.llm,
                browser_profile=self.browser_profile,
                max_actions_per_step=1,
                use_vision=True,
                save_screenshots=False,
                extend_system_message="Complete TopSurveys survey using persona data. Handle all question types systematically.",
            )

            # Run survey completion
            start_time = time.time()
            history = await agent.run(max_steps=120)  # More time for surveys
            end_time = time.time()

            # Analyze completion
            result = {
                'status': 'completed',
                'duration': round(end_time - start_time, 2),
                'steps_taken': len(history.action_results) if hasattr(history, 'action_results') else 0,
                'timestamp': datetime.now().isoformat(),
                'platform': 'topsurveys',
                'completion_method': 'topsurveys_specialized'
            }

            # Check completion status
            if hasattr(history, 'final_result') and history.final_result:
                result_text = history.final_result

                if "disqualified" in result_text.lower():
                    result['status'] = 'disqualified'
                    logger.info("❌ Disqualified from survey")
                elif "completed" in result_text.lower() or "submitted" in result_text.lower():
                    result['status'] = 'completed'
                    logger.info("✅ Survey completed successfully!")
                else:
                    result['status'] = 'unknown'
                    logger.warning(f"⚠️ Unknown completion status: {result_text}")
            else:
                result['status'] = 'unknown'
                logger.warning("⚠️ No completion result available")

            return result

        except Exception as e:
            logger.error(f"Survey completion failed: {e}")
            return {
                'status': 'failed',
                'error': str(e),
                'timestamp': datetime.now().isoformat(),
                'platform': 'topsurveys',
                'completion_method': 'topsurveys_specialized'
            }

    async def run_topsurveys_session(self, max_surveys: int = 2) -> Dict[str, Any]:
        """Run a complete TopSurveys session."""
        logger.info("Starting TopSurveys automation session...")

        session_start = datetime.now()
        completed_count = 0
        disqualified_count = 0
        failed_count = 0

        try:
            # Step 1: Login to TopSurveys
            logger.info("🔐 Step 1: Logging into TopSurveys...")
            login_success = await self.perform_topsurveys_login()

            if not login_success:
                logger.error("❌ Login failed, cannot proceed")
                return {
                    'error': 'TopSurveys login failed',
                    'completed': 0,
                    'disqualified': 0,
                    'failed': 0,
                    'session_duration': (datetime.now() - session_start).total_seconds()
                }

            logger.info("✅ Successfully logged into TopSurveys!")

            # Step 2: Complete surveys
            for i in range(max_surveys):
                logger.info(f"📝 Step 2.{i+1}: Survey {i+1}/{max_surveys}")

                # Find and start a survey
                survey_found = await self.discover_available_surveys()

                if not survey_found:
                    logger.warning(f"No survey found for attempt {i+1}")
                    await asyncio.sleep(3)  # Wait before next attempt
                    continue

                # Complete the survey
                result = await self.complete_topsurveys_survey()

                # Track results
                if result['status'] == 'completed':
                    completed_count += 1
                    self.completed_surveys.append(result)
                    logger.info(f"✅ Survey {i+1} completed!")
                elif result['status'] == 'disqualified':
                    disqualified_count += 1
                    logger.info(f"❌ Survey {i+1} disqualified")
                else:
                    failed_count += 1
                    self.failed_surveys.append(result)
                    logger.info(f"⚠️ Survey {i+1} failed")

                # Progress update
                logger.info(f"Progress: {completed_count} completed, {disqualified_count} disqualified, {failed_count} failed")

                # Wait between surveys
                if i < max_surveys - 1:
                    logger.info("⏳ Waiting 8 seconds before next survey...")
                    await asyncio.sleep(8)

            # Session summary
            session_duration = (datetime.now() - session_start).total_seconds()

            logger.info("🎉 TopSurveys session complete!")
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
                'platform': 'topsurveys',
                'specializations': [
                    'topsurveys_workflow_optimization',
                    'specialized_login_handling',
                    'survey_discovery_algorithms',
                    'persona_driven_completion',
                    'platform_specific_error_handling'
                ]
            }

        except Exception as e:
            logger.error(f"TopSurveys session failed: {e}")
            return {
                'error': str(e),
                'completed': completed_count,
                'disqualified': disqualified_count,
                'failed': failed_count,
                'session_duration': (datetime.now() - session_start).total_seconds()
            }

async def main():
    """Main function to run TopSurveys automation."""
    print("🎯 TopSurveys-Specific Survey Automation Bot")
    print("=" * 50)

    # Initialize TopSurveys bot
    try:
        bot = TopSurveysBot()
        print("✅ TopSurveys bot initialized successfully")
        print("🎯 Specialized for TopSurveys platform workflow")
        print("🧠 Using persona: Jordan Mitchell")
    except Exception as e:
        print(f"❌ Failed to initialize TopSurveys bot: {e}")
        return

    # Run TopSurveys session
    print("\n🚀 Starting TopSurveys automation session...")
    print("Specializations:")
    print("  ✅ TopSurveys-specific login workflow")
    print("  ✅ Survey discovery algorithms")
    print("  ✅ Platform-specific error handling")
    print("  ✅ Optimized for survey completion")
    print("  ✅ ChromeOS compatibility")

    results = await bot.run_topsurveys_session(max_surveys=2)

    # Print results
    print("\n📊 TopSurveys Session Results:")
    print("=" * 35)
    print(f"✅ Surveys Completed: {results.get('completed', 0)}")
    print(f"❌ Surveys Disqualified: {results.get('disqualified', 0)}")
    print(f"⚠️  Surveys Failed: {results.get('failed', 0)}")

    if 'session_duration' in results:
        print(f"⏱️  Session Duration: {results['session_duration']:.1f} seconds")

    if results.get('specializations'):
        print("🔧 Specializations Applied:")
        for spec in results['specializations']:
            print(f"   • {spec}")

    if results.get('error'):
        print(f"💥 Error: {results['error']}")

    print("\n🎉 TopSurveys automation complete!")

if __name__ == "__main__":
    asyncio.run(main())
