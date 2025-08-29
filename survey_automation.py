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
        logging.FileHandler('survey_automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SurveyAutomationBot:
    def __init__(self):
        """Initialize the survey automation bot."""
        self.login_email = "marerise28@gmail.com"
        self.login_password = "iinqxnE%kuA#!Evubr3q%"
        self.base_url = "https://app.topsurveys.app/Surveys"
        
        # Initialize Gemini LLM for survey intelligence
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        self.llm = ChatGoogle(
            model='gemini-2.0-flash-exp',
            api_key=api_key,
            temperature=0.1  # Low temperature for consistent behavior
        )
        
        # Browser profile optimized for survey sites on ChromeOS
        self.browser_profile = BrowserProfile(
            headless=True,  # Use headless mode for ChromeOS compatibility
            minimum_wait_page_load_time=1.0,
            wait_between_actions=0.5,
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
        
        # Survey completion tracking
        self.completed_surveys = []
        self.failed_surveys = []
        
        logger.info("Survey automation bot initialized successfully")
    
    def _load_persona_data(self) -> Dict[str, Any]:
        """Load persona data for intelligent survey responses."""
        try:
            with open('persona.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load persona data: {e}")
            raise
    
    def _create_survey_task(self, survey_url: Optional[str] = None) -> str:
        """Create a comprehensive survey completion task."""
        
        task = f"""
You are an intelligent survey completion assistant. Your goal is to complete surveys efficiently and realistically.

CURRENT TASK: Complete the survey at {survey_url or 'the current survey page'}

GENERAL INSTRUCTIONS:
1. **Login Process**: If not already logged in, use these credentials:
   - Email: {self.login_email}
   - Password: {self.login_password}

2. **Survey Navigation**:
   - Look for available surveys on the main dashboard
   - Click on surveys that match your persona's interests and demographics
   - Navigate through pre-screening questions carefully

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

6. **Error Handling**:
   - If a survey is unavailable or you encounter errors, move to the next one
   - Don't get stuck on any single survey
   - Log all activities for monitoring

7. **Quality Assurance**:
   - Answer thoughtfully and realistically
   - Don't rush through questions
   - Maintain consistency with your persona throughout

STARTING POINT: Begin at {self.base_url} and systematically work through available surveys.
"""
        return task
    
    def _is_open_ended_question(self, question_text: str) -> bool:
        """Check if a question requires personality-driven response."""
        open_ended_keywords = [
            'why', 'how', 'what do you think', 'describe', 'explain', 'tell me about',
            'what are your thoughts', 'how do you feel', 'what is your opinion',
            'share your experience', 'what would you', 'how has', 'what was',
            'can you tell me', 'what are you', 'how are you', 'what do you like'
        ]
        
        question_lower = question_text.lower()
        return any(keyword in question_lower for keyword in open_ended_keywords)
    
    async def _handle_open_ended_question(self, question_text: str, context: str = "") -> str:
        """Handle open-ended questions with personality-driven responses."""
        try:
            response = await generate_personality_response(question_text, context)
            logger.info(f"Generated personality response: {response[:100]}...")
            return response
        except Exception as e:
            logger.error(f"Failed to generate personality response: {e}")
            return "I appreciate you asking. This is an interesting topic that I'd be happy to share my thoughts on."
    
    async def run_single_survey(self, survey_url: str, max_steps: int = 50) -> Dict[str, Any]:
        """Run a single survey with comprehensive error handling."""
        
        logger.info(f"Starting survey: {survey_url}")
        
        try:
            # Create agent for this survey
            agent = Agent(
                task=self._create_survey_task(survey_url),
                llm=self.llm,
                browser_profile=self.browser_profile,
                max_actions_per_step=1,  # Careful, methodical approach
                use_vision=True,  # Important for reading survey questions
                save_screenshots=False,  # Reduce overhead
            )
            
            # Run the survey
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
                'errors': []
            }
            
            # Check if survey was actually completed
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
            logger.error(f"Failed to complete survey {survey_url}: {e}")
            return {
                'survey_url': survey_url,
                'status': 'failed',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    async def run_continuous_survey_loop(self, max_surveys: int = 10, delay_between_surveys: int = 5):
        """Run continuous survey completion loop."""
        
        logger.info(f"Starting continuous survey loop (max {max_surveys} surveys)")
        
        completed_count = 0
        disqualified_count = 0
        failed_count = 0
        
        try:
            # Start with the main survey page
            current_url = self.base_url
            
            for i in range(max_surveys):
                logger.info(f"=== Survey {i+1}/{max_surveys} ===")
                
                # Run the survey
                result = await self.run_single_survey(current_url, max_steps=100)
                
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
                logger.info(f"Progress: {completed_count} completed, {disqualified_count} disqualified, {failed_count} failed")
                
                # Add delay between surveys to be respectful
                if i < max_surveys - 1:  # Don't delay after the last survey
                    logger.info(f"Waiting {delay_between_surveys} seconds before next survey...")
                    await asyncio.sleep(delay_between_surveys)
                
                # Check if we should continue
                if failed_count >= 3:  # Stop if too many failures
                    logger.warning("Too many failed surveys, stopping loop")
                    break
            
            # Final summary
            logger.info("=== Survey Loop Complete ===")
            logger.info(f"Final Results:")
            logger.info(f"  Completed: {completed_count}")
            logger.info(f"  Disqualified: {disqualified_count}")
            logger.info(f"  Failed: {failed_count}")
            
            return {
                'completed': completed_count,
                'disqualified': disqualified_count,
                'failed': failed_count,
                'completed_surveys': self.completed_surveys,
                'failed_surveys': self.failed_surveys
            }
            
        except Exception as e:
            logger.error(f"Survey loop failed: {e}")
            return {
                'error': str(e),
                'completed': completed_count,
                'disqualified': disqualified_count,
                'failed': failed_count
            }

async def main():
    """Main function to run the survey automation."""
    
    print("🤖 Survey Automation Bot Starting...")
    print("=====================================")
    
    # Initialize bot
    try:
        bot = SurveyAutomationBot()
        print("✅ Bot initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize bot: {e}")
        return
    
    # Run continuous survey loop
    print("\n🚀 Starting survey automation loop...")
    print("This will automatically:")
    print("  - Login to TopSurveys")
    print("  - Find available surveys")
    print("  - Complete qualifying surveys")
    print("  - Handle open-ended questions with personality")
    print("  - Continue until completion or errors")
    
    results = await bot.run_continuous_survey_loop(
        max_surveys=10,  # Adjust as needed
        delay_between_surveys=3
    )
    
    # Print final results
    print("\n📊 Final Results:")
    print("==================")
    print(f"✅ Surveys Completed: {results.get('completed', 0)}")
    print(f"❌ Surveys Disqualified: {results.get('disqualified', 0)}")
    print(f"⚠️  Surveys Failed: {results.get('failed', 0)}")
    
    if results.get('error'):
        print(f"💥 Error: {results['error']}")
    
    print("\n🎉 Survey automation complete!")

if __name__ == "__main__":
    asyncio.run(main())
