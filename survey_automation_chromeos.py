#!/usr/bin/env python3
"""
ChromeOS-compatible Survey Automation Bot
This version is optimized for ChromeOS environments with browser restrictions
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
        logging.FileHandler('survey_automation_chromeos.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ChromeOSSurveyBot:
    def __init__(self):
        """Initialize the ChromeOS-compatible survey automation bot."""
        self.login_email = "marerise28@gmail.com"
        self.login_password = "iinqxnE%kuA#!Evubr3q%"
        self.base_url = "https://app.topsurveys.app/Surveys"
        
        # Initialize Gemini LLM
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        self.llm = ChatGoogle(
            model='gemini-2.0-flash-exp',
            api_key=api_key,
            temperature=0.1
        )
        
        # ChromeOS-optimized browser profile
        self.browser_profile = BrowserProfile(
            headless=True,  # Use headless mode for ChromeOS compatibility
            minimum_wait_page_load_time=2.0,  # Longer wait for ChromeOS
            wait_between_actions=1.0,  # Slower actions for stability
            viewport_width=1200,
            viewport_height=800,
            # ChromeOS-specific browser arguments
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
            ]
        )
        
        # Load persona data
        self.persona_data = self._load_persona_data()
        
        # Survey tracking
        self.completed_surveys = []
        self.failed_surveys = []
        
        logger.info("ChromeOS-compatible survey automation bot initialized")
    
    def _load_persona_data(self) -> Dict[str, Any]:
        """Load persona data for intelligent survey responses."""
        try:
            with open('persona.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load persona data: {e}")
            raise
    
    def _create_chromeos_survey_task(self, survey_url: Optional[str] = None) -> str:
        """Create a ChromeOS-optimized survey completion task."""
        
        task = f"""
You are an intelligent survey completion assistant optimized for ChromeOS environments.

CURRENT TASK: Complete the survey at {survey_url or 'the current survey page'}

CHROMEOS OPTIMIZATIONS:
- Use slower, more deliberate actions for stability
- Wait longer between page loads and interactions
- Handle any ChromeOS-specific browser limitations gracefully
- Use Playwright's enhanced element detection

GENERAL INSTRUCTIONS:
1. **Login Process**: If not already logged in, use these credentials:
   - Email: {self.login_email}
   - Password: {self.login_password}
   - Be patient with ChromeOS browser initialization

2. **Survey Navigation**:
   - Look for available surveys on the main dashboard
   - Click on surveys that match your persona's interests and demographics
   - Navigate through pre-screening questions carefully
   - Use longer waits between actions for ChromeOS stability

3. **Pre-screening Questions**:
   - Answer based on your persona: {self.persona_data['about_you']['full_name']}, {self.persona_data['about_you']['age']}-year-old {self.persona_data['about_you']['occupation']} from {self.persona_data['about_you']['city']}, {self.persona_data['about_you']['state']}
   - Key demographics: Married with {self.persona_data['family_and_household']['children']}, household income {self.persona_data['family_and_household']['combined_household_income']}
   - Be honest about qualifications - if you don't qualify, acknowledge it

4. **Open-Ended Questions**:
   - When you encounter open-ended questions (containing words like "why", "how", "what do you think", "describe", "explain")
   - Generate natural, personality-driven responses using the personality system
   - Keep responses 2-4 sentences, conversational, and authentic

5. **Survey Completion**:
   - Complete the entire survey if you qualify
   - If you don't qualify for pre-screening, acknowledge it and return to survey selection
   - Submit the survey when finished
   - Return to the main dashboard to find the next survey

6. **ChromeOS Error Handling**:
   - If browser crashes or becomes unresponsive, wait and retry
   - Handle any permission or security dialogs that may appear
   - Be patient with slower page loads on ChromeOS
   - Don't get stuck on any single survey

7. **Quality Assurance**:
   - Answer thoughtfully and realistically
   - Don't rush through questions
   - Maintain consistency with your persona throughout
   - Use ChromeOS-appropriate timing

STARTING POINT: Begin at {self.base_url} and systematically work through available surveys with ChromeOS-optimized behavior.
"""
        return task
    
    async def run_chromeos_survey(self, survey_url: str, max_steps: int = 60) -> Dict[str, Any]:
        """Run a single survey with ChromeOS optimizations."""
        
        logger.info(f"Starting ChromeOS-optimized survey: {survey_url}")
        
        try:
            # Create ChromeOS-optimized agent
            agent = Agent(
                task=self._create_chromeos_survey_task(survey_url),
                llm=self.llm,
                browser_profile=self.browser_profile,
                max_actions_per_step=1,  # Single action per step for stability
                use_vision=True,  # Important for reading survey questions
                save_screenshots=False,  # Reduce overhead
                # ChromeOS-specific settings
                extend_system_message="Use ChromeOS-optimized behavior: slower actions, longer waits, and graceful error handling.",
            )
            
            # Run the survey with ChromeOS optimizations
            start_time = time.time()
            history = await agent.run(max_steps=max_steps)
            end_time = time.time()
            
            # Analyze results
            result = {
                'survey_url': survey_url,
                'status': 'completed',
                'duration': round(end_time - start_time, 2),
                'steps_taken': len(history.action_results) if hasattr(history, 'action_results') else 0,
                'timestamp': datetime.now().isoformat(),
                'chromeos_optimizations': True,
                'errors': []
            }
            
            # Check completion status
            final_url = history.final_result.url if hasattr(history, 'final_result') else ""
            
            if "qualify" in final_url.lower() or "disqualified" in final_url.lower():
                result['status'] = 'disqualified'
                logger.info(f"Disqualified from survey: {survey_url}")
            elif self.base_url in final_url or "surveys" in final_url.lower():
                result['status'] = 'completed'
                logger.info(f"Successfully completed survey: {survey_url}")
            else:
                result['status'] = 'unknown'
                logger.warning(f"Unknown completion status for survey: {survey_url}")
            
            return result
            
        except Exception as e:
            logger.error(f"ChromeOS survey failed: {survey_url} - {e}")
            return {
                'survey_url': survey_url,
                'status': 'failed',
                'error': str(e),
                'timestamp': datetime.now().isoformat(),
                'chromeos_optimizations': True
            }
    
    async def run_chromeos_survey_loop(self, max_surveys: int = 5, delay_between_surveys: int = 10):
        """Run ChromeOS-optimized continuous survey completion loop."""
        
        logger.info(f"Starting ChromeOS-optimized survey loop (max {max_surveys} surveys)")
        
        completed_count = 0
        disqualified_count = 0
        failed_count = 0
        
        try:
            current_url = self.base_url
            
            for i in range(max_surveys):
                logger.info(f"=== ChromeOS Survey {i+1}/{max_surveys} ===")
                
                # Run ChromeOS-optimized survey
                result = await self.run_chromeos_survey(current_url, max_steps=80)
                
                # Track results
                if result['status'] == 'completed':
                    completed_count += 1
                    self.completed_surveys.append(result)
                elif result['status'] == 'disqualified':
                    disqualified_count += 1
                else:
                    failed_count += 1
                    self.failed_surveys.append(result)
                
                # Log progress
                logger.info(f"ChromeOS Progress: {completed_count} completed, {disqualified_count} disqualified, {failed_count} failed")
                
                # Longer delay between surveys for ChromeOS stability
                if i < max_surveys - 1:
                    logger.info(f"Waiting {delay_between_surveys} seconds before next survey (ChromeOS optimization)...")
                    await asyncio.sleep(delay_between_surveys)
                
                # Stop if too many failures
                if failed_count >= 2:  # Lower threshold for ChromeOS
                    logger.warning("Too many failed surveys on ChromeOS, stopping loop")
                    break
            
            # Final summary
            logger.info("=== ChromeOS Survey Loop Complete ===")
            logger.info(f"Final Results:")
            logger.info(f"  Completed: {completed_count}")
            logger.info(f"  Disqualified: {disqualified_count}")
            logger.info(f"  Failed: {failed_count}")
            
            return {
                'completed': completed_count,
                'disqualified': disqualified_count,
                'failed': failed_count,
                'completed_surveys': self.completed_surveys,
                'failed_surveys': self.failed_surveys,
                'chromeos_optimized': True
            }
            
        except Exception as e:
            logger.error(f"ChromeOS survey loop failed: {e}")
            return {
                'error': str(e),
                'completed': completed_count,
                'disqualified': disqualified_count,
                'failed': failed_count,
                'chromeos_optimized': True
            }

async def main():
    """Main function to run the ChromeOS-compatible survey automation."""
    
    print("🤖 ChromeOS-Compatible Survey Automation Bot")
    print("=============================================")
    
    # Initialize ChromeOS bot
    try:
        bot = ChromeOSSurveyBot()
        print("✅ ChromeOS bot initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize ChromeOS bot: {e}")
        return
    
    # Run ChromeOS-optimized survey loop
    print("\n🚀 Starting ChromeOS-optimized survey automation...")
    print("ChromeOS optimizations:")
    print("  ✅ Slower, more stable browser actions")
    print("  ✅ Longer waits for page loads")
    print("  ✅ Playwright-enhanced element detection")
    print("  ✅ Graceful error handling for ChromeOS")
    print("  ✅ Reduced survey count for stability")
    
    results = await bot.run_chromeos_survey_loop(
        max_surveys=5,  # Reduced for ChromeOS stability
        delay_between_surveys=10  # Longer delays for ChromeOS
    )
    
    # Print ChromeOS results
    print("\n📊 ChromeOS Survey Results:")
    print("============================")
    print(f"✅ Surveys Completed: {results.get('completed', 0)}")
    print(f"❌ Surveys Disqualified: {results.get('disqualified', 0)}")
    print(f"⚠️  Surveys Failed: {results.get('failed', 0)}")
    
    if results.get('chromeos_optimized'):
        print("🖥️  ChromeOS optimizations applied")
    
    if results.get('error'):
        print(f"💥 Error: {results['error']}")
    
    print("\n🎉 ChromeOS survey automation complete!")

if __name__ == "__main__":
    asyncio.run(main())
