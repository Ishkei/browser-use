#!/usr/bin/env python3
"""
ChromeOS Startup Script for Survey Automation Bot
Optimized for ChromeOS environments
"""

import os
import sys
from pathlib import Path

def check_chromeos_environment():
    """Check if the environment is properly set up for ChromeOS."""
    print("🔍 Checking ChromeOS environment...")
    
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
            print("   Virtual environment found at .venv/")
        else:
            print("❌ Virtual environment not found!")
            print("   Run: source .venv/bin/activate")
            return False
    
    print("✅ ChromeOS environment check passed!")
    return True

def run_chromeos_survey_bot():
    """Run the ChromeOS-compatible survey automation bot."""
    print("\n🚀 Starting ChromeOS Survey Automation Bot...")
    print("=" * 60)
    
    try:
        # Import and run the ChromeOS bot
        from survey_automation_chromeos import main
        import asyncio
        
        print("✅ ChromeOS bot imported successfully!")
        print("🎭 Using persona: Jordan Mitchell")
        print("🔐 Target: TopSurveys platform")
        print("🧠 AI: Google Gemini powered responses")
        print("🖥️  Optimized for ChromeOS")
        print()
        
        # Run the ChromeOS bot
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
    """Main ChromeOS startup function."""
    print("🤖 ChromeOS Survey Automation Bot - Startup")
    print("=" * 60)
    
    # Check environment
    if not check_chromeos_environment():
        print("\n❌ Environment setup incomplete!")
        print("   Please fix the issues above and try again.")
        return 1
    
    # Run the ChromeOS bot
    if run_chromeos_survey_bot():
        print("\n🎉 ChromeOS survey automation completed successfully!")
        return 0
    else:
        print("\n💥 ChromeOS survey automation failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
