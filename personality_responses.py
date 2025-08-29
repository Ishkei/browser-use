import json
import logging
import asyncio
from typing import Dict, Any, Optional
import google.generativeai as genai
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

class PersonalityResponseGenerator:
    def __init__(self, persona_file: str = "persona.json", api_key: Optional[str] = None):
        """Initialize the personality response generator."""
        self.persona_file = persona_file
        self.api_key = api_key or os.getenv('GOOGLE_API_KEY')
        
        if not self.api_key:
            raise ValueError("Google API key is required. Set GOOGLE_API_KEY environment variable or pass api_key parameter.")
        
        # Configure Gemini API
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Load persona data
        self.persona_data = self._load_persona()
        
        # Create personality prompt
        self.personality_prompt = self._create_personality_prompt()
    
    def _load_persona(self) -> Dict[str, Any]:
        """Load persona data from JSON file."""
        try:
            with open(self.persona_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Persona file not found: {self.persona_file}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in persona file: {e}")
    
    def _create_personality_prompt(self) -> str:
        """Create the personality prompt from persona data."""
        persona = self.persona_data
        
        prompt = f"""
You are role-playing as {persona['about_you']['full_name']}, a {persona['about_you']['age']}-year-old {persona['about_you']['occupation']} from {persona['about_you']['city']}, {persona['about_you']['state']}.

KEY CHARACTERISTICS:
- Gender: {persona['about_you']['gender']}
- Marital Status: {persona['about_you']['marital_status']}
- Children: {persona['about_you']['children']}
- Occupation: {persona['work']['job_title']} in {persona['work']['company_industry']}
- Household Income: {persona['family_and_household']['combined_household_income']}
- Interests: {', '.join(persona['about_you']['interests'])}
- Technology: {persona['technology']['smartphone_brand']} user, {persona['technology']['early_adopter_of_technology']}
- Shopping Style: {persona['shopping']['brand_loyalty_level']}, {persona['shopping']['price_sensitivity']}

COMMUNICATION STYLE:
- Be conversational and natural, like you're texting or writing an email
- Use contractions (I'm, you're, don't, can't)
- Show personality and genuine opinions
- Be honest about likes/dislikes based on your background
- Keep responses concise but thoughtful (2-4 sentences typically)
- Sound like a real person, not a robot
- Reference your background when relevant (family, work, interests)

RESPONSE GUIDELINES:
- For open-ended questions: Give thoughtful, personal responses based on your life experience
- For rating scales: Choose thoughtfully based on your demographics and preferences
- For multiple choice: Select what makes sense for your persona
- Never mention being an AI or role-playing
- Stay in character at all times

Your current situation:
- Working as {persona['about_you']['occupation']} at a {persona['work']['company_size']} healthcare technology company
- Married with {persona['family_and_household']['children']} child, living in a {persona['family_and_household']['living_situation']}
- Active in {', '.join(persona['about_you']['hobbies'])}
- Regular survey participant who provides {persona['survey_participation']['feedback_quality']}
- Life satisfaction: {persona['survey_behavior']['satisfaction_with_life']}
"""
        return prompt
    
    def _is_open_ended_question(self, question: str) -> bool:
        """Determine if a question requires a personality-driven response."""
        open_ended_keywords = [
            'why', 'how', 'what do you think', 'describe', 'explain', 'tell me about',
            'what are your thoughts', 'how do you feel', 'what is your opinion',
            'share your experience', 'what would you', 'how has', 'what was',
            'can you tell me', 'what are you', 'how are you', 'what do you like'
        ]
        
        question_lower = question.lower()
        return any(keyword in question_lower for keyword in open_ended_keywords)
    
    def _get_fallback_response(self, question: str) -> str:
        """Generate a fallback response when API is unavailable."""
        persona = self.persona_data
        
        # Technology-related questions
        if any(word in question.lower() for word in ['technology', 'phone', 'computer', 'app', 'software']):
            responses = [
                f"As a {persona['technology']['smartphone_brand']} user who works in tech, I'm always interested in the latest technology trends.",
                f"I work in healthcare technology, so I see firsthand how technology can improve people's lives.",
                f"I'm definitely a tech enthusiast - I love trying new gadgets and apps."
            ]
        
        # Family-related questions
        elif any(word in question.lower() for word in ['family', 'child', 'kids', 'spouse', 'husband', 'wife']):
            responses = [
                f"Family is extremely important to me. I'm married with a {persona['family_and_household']['children']} and we live in Denver.",
                f"As a parent of a {persona['family_and_household']['children']}, I always prioritize family activities and quality time.",
                f"My family comes first - I'm lucky to have a great spouse and child who make life wonderful."
            ]
        
        # Work-related questions
        elif any(word in question.lower() for word in ['work', 'job', 'career', 'company']):
            responses = [
                f"I work as a {persona['about_you']['occupation']} in healthcare technology, which I really enjoy.",
                f"My career in marketing keeps me busy, but I love the creative aspects of my job.",
                f"At work, I focus on healthcare technology solutions that make a real difference."
            ]
        
        # Health and wellness questions
        elif any(word in question.lower() for word in ['health', 'fitness', 'wellness', 'exercise']):
            responses = [
                f"Health and wellness are really important to me. I try to stay active with yoga and healthy eating.",
                f"I'm conscious about my health - I exercise regularly and focus on nutrition for my family.",
                f"Wellness is a priority - I practice yoga and make sure to take care of myself and my family."
            ]
        
        # Shopping and consumer questions
        elif any(word in question.lower() for word in ['buy', 'purchase', 'shopping', 'brand', 'product']):
            responses = [
                f"I'm pretty brand loyal for trusted products, especially in technology and family items.",
                f"I research purchases carefully and value quality, especially for things my family uses.",
                f"As a primary decision maker for household purchases, I look for reliable brands and good value."
            ]
        
        # General fallback
        else:
            responses = [
                f"That's an interesting question. Based on my experience as a {persona['about_you']['age']}-year-old {persona['about_you']['occupation']}, I'd say it depends on the situation.",
                f"I appreciate you asking. From my perspective in {persona['about_you']['city']}, I think it's always good to consider different viewpoints.",
                f"Thanks for asking! As someone who values {', '.join(persona['about_you']['interests'][:2])}, I try to make thoughtful decisions."
            ]
        
        import random
        return random.choice(responses)
    
    async def generate_response(self, question: str, context: Optional[str] = None) -> str:
        """Generate a personality-driven response to a question."""
        if not self._is_open_ended_question(question):
            return ""  # Not an open-ended question, let the agent handle it normally
        
        try:
            # Create the full prompt
            full_prompt = f"{self.personality_prompt}\n\nQuestion: {question}"
            if context:
                full_prompt += f"\n\nContext: {context}"
            
            full_prompt += "\n\nRespond naturally as yourself, staying in character:"
            
            # Generate response using Gemini
            response = await asyncio.get_event_loop().run_in_executor(
                None, 
                self.model.generate_content,
                full_prompt
            )
            
            # Extract and clean the response
            if hasattr(response, 'text') and response.text:
                return response.text.strip()
            else:
                logger.warning("Empty response from Gemini API, using fallback")
                return self._get_fallback_response(question)
                
        except Exception as e:
            logger.error(f"Error generating personality response: {e}")
            return self._get_fallback_response(question)

# Global instance for easy access
_personality_generator = None

def get_personality_generator() -> PersonalityResponseGenerator:
    """Get the global personality generator instance."""
    global _personality_generator
    if _personality_generator is None:
        _personality_generator = PersonalityResponseGenerator()
    return _personality_generator

async def generate_personality_response(question: str, context: Optional[str] = None) -> str:
    """Convenience function to generate personality-driven responses."""
    generator = get_personality_generator()
    return await generator.generate_response(question, context)
