#!/usr/bin/env python3
"""
Simple startup script for Survey Automation Bot
Runs locally without Docker requirements
"""

import os
import sys
import subprocess
from pathlib import Path

def check_environment():
    """Check if the environment is properly set up."""
    print("🔍 Checking environment...")
    
    # Check if .env exists
    if not Path('.env').exists():
        print("❌ .env file not found!")
        print("   Please ensure your API keys are configured.")
        return False
    
    # Check if persona.json exists
    if not Path('persona.json').exists():
        print("❌ persona.json not found!")
        print("   Please ensure your persona data is configured.")
        return False
    
    # Check if virtual environment is active
    if not os.getenv('VIRTUAL_ENV'):
        print("⚠️  Virtual environment not active, activating...")
        venv_path = Path('.venv/bin/activate')
        if venv_path.exists():
            # Note: This won't actually activate in the parent shell
            print("   Virtual environment found at .venv/")
        else:
            print("❌ Virtual environment not found!")
            print("   Run: source .venv/bin/activate")
            return False
    
    print("✅ Environment check passed!")
    return True

def run_survey_bot():
    """Run the survey automation bot."""
    print("\n🚀 Starting Survey Automation Bot...")
    print("=" * 50)
    
    try:
        # Import and run the bot
        from survey_automation import main
        import asyncio
        
        print("✅ Bot imported successfully!")
        print("🎭 Using persona: Jordan Mitchell")
        print("🔐 Target: TopSurveys platform")
        print("🧠 AI: Google Gemini powered responses")
        print()
        
        # Run the bot
        asyncio.run(main())
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure all dependencies are installed:")
        print("   source .venv/bin/activate")
        print("   uv sync")
        return False
    except Exception as e:
        print(f"❌ Runtime error: {e}")
        return False
    
    return True

def main():
    """Main startup function."""
    print("🤖 Survey Automation Bot - Local Startup")
    print("=" * 50)
    
    # Check environment
    if not check_environment():
        print("\n❌ Environment setup incomplete!")
        print("   Please fix the issues above and try again.")
        return 1
    
    # Run the bot
    if run_survey_bot():
        print("\n🎉 Survey automation completed successfully!")
        return 0
    else:
        print("\n💥 Survey automation failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
