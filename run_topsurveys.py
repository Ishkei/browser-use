#!/usr/bin/env python3
"""
TopSurveys-Specific Survey Automation Runner
Runs the highly optimized TopSurveys automation
"""

import os
import sys
from pathlib import Path

def check_topsurveys_environment():
    """Check if the environment is properly set up for TopSurveys automation."""
    print("🔍 Checking TopSurveys environment...")

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

    # Check if TopSurveys script exists
    if not Path('survey_automation_topsurveys.py').exists():
        print("❌ survey_automation_topsurveys.py not found!")
        print("   Please ensure the TopSurveys script is available.")
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

    print("✅ TopSurveys environment check passed!")
    return True

def run_topsurveys_bot():
    """Run the TopSurveys-specific survey automation bot."""
    print("\n🚀 Starting TopSurveys-Specific Survey Automation Bot...")
    print("=" * 60)

    try:
        # Import and run the TopSurveys bot
        from survey_automation_topsurveys import main
        import asyncio

        print("✅ TopSurveys bot imported successfully!")
        print("🎯 Specialized for TopSurveys platform workflow")
        print("🧠 Using persona: Jordan Mitchell")
        print("⚡ TopSurveys Optimizations:")
        print("   • TopSurveys-specific login workflow")
        print("   • Survey discovery algorithms")
        print("   • Platform-specific error handling")
        print("   • Optimized for survey completion")
        print("   • ChromeOS compatibility")
        print()

        # Run the TopSurveys bot
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
    """Main TopSurveys runner function."""
    print("🎯 TopSurveys Survey Automation Runner")
    print("=" * 42)

    # Check environment
    if not check_topsurveys_environment():
        print("\n❌ Environment setup incomplete!")
        print("   Please fix the issues above and try again.")
        return 1

    # Run the TopSurveys bot
    if run_topsurveys_bot():
        print("\n🎉 TopSurveys automation completed successfully!")
        return 0
    else:
        print("\n💥 TopSurveys automation failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
