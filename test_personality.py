import asyncio
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from personality_responses import generate_personality_response, PersonalityResponseGenerator

async def test_personality_system():
    """Test the personality response system."""
    
    print("🧪 Testing Personality Response System")
    print("=======================================")
    
    # Test questions
    test_questions = [
        "Why did you join this survey platform?",
        "What do you think about technology in healthcare?",
        "How do you balance work and family life?",
        "What are your thoughts on sustainable living?",
        "Why is family important to you?",
        "How has technology influenced your daily life?",
        "What do you like most about your job?",
        "How do you make purchasing decisions for your family?"
    ]
    
    print("Testing personality-driven responses:")
    print("-" * 50)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Question: {question}")
        try:
            response = await generate_personality_response(question)
            print(f"   Response: {response}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n✅ Personality system test complete!")

async def test_open_ended_detection():
    """Test open-ended question detection."""
    
    print("\n🔍 Testing Open-Ended Question Detection")
    print("=========================================")
    
    generator = PersonalityResponseGenerator()
    
    test_questions = [
        "What is your age?",  # Not open-ended
        "Why do you think that?",  # Open-ended
        "How old are you?",  # Not open-ended
        "What are your thoughts on this?",  # Open-ended
        "Select your income range:",  # Not open-ended
        "How has this affected you?",  # Open-ended
    ]
    
    for question in test_questions:
        is_open_ended = generator._is_open_ended_question(question)
        status = "📝 OPEN-ENDED" if is_open_ended else "🔘 CLOSED-ENDED"
        print(f"{status}: {question}")

async def main():
    """Run all tests."""
    
    print("🚀 Starting Personality System Tests")
    print("=" * 50)
    
    try:
        await test_open_ended_detection()
        await test_personality_system()
        
        print("\n🎉 All tests completed successfully!")
        
    except Exception as e:
        print(f"\n💥 Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
