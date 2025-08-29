#!/usr/bin/env python3
"""
Improved Survey Automation Runner
Runs the optimized TopSurveys automation
"""

import os
import sys
from pathlib import Path

def check_improved_environment():
    """Check if the environment is properly set up for improved automation."""
    print("🔍 Checking improved environment...")

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

    # Check if improved script exists
    if not Path('survey_automation_improved.py').exists():
        print("❌ survey_automation_improved.py not found!")
        print("   Please ensure the improved script is available.")
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

    print("✅ Improved environment check passed!")
    return True

def run_improved_bot():
    """Run the improved survey automation bot."""
    print("\n🚀 Starting Improved Survey Automation Bot...")
    print("=" * 55)

    try:
        # Import and run the improved bot
        from survey_automation_improved import main
        import asyncio

        print("✅ Improved bot imported successfully!")
        print("🎯 Specialized for TopSurveys platform")
        print("🧠 Using persona: Jordan Mitchell")
        print("⚡ Optimized with:")
        print("   • Precise login flow")
        print("   • Better element detection")
        print("   • Survey discovery agent")
        print("   • Improved error handling")
        print()

        # Run the improved bot
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
    """Main improved runner function."""
    print("🤖 Improved TopSurveys Automation Runner")
    print("=" * 45)

    # Check environment
    if not check_improved_environment():
        print("\n❌ Environment setup incomplete!")
        print("   Please fix the issues above and try again.")
        return 1

    # Run the improved bot
    if run_improved_bot():
        print("\n🎉 Improved survey automation completed successfully!")
        return 0
    else:
        print("\n💥 Improved survey automation failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())
