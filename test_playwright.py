#!/usr/bin/env python3
"""
Simple Playwright test to verify browser launch works on ChromeOS
"""

import asyncio
from playwright.async_api import async_playwright

async def test_playwright_launch():
    """Test if Playwright can launch a browser on ChromeOS."""
    
    print("🧪 Testing Playwright browser launch on ChromeOS...")
    
    try:
        async with async_playwright() as p:
            print("✅ Playwright context created successfully")
            
            # Try to launch Chromium
            browser = await p.chromium.launch(
                headless=False,  # Keep visible for testing
                args=['--no-sandbox', '--disable-dev-shm-usage']  # ChromeOS compatibility
            )
            print("✅ Chromium browser launched successfully")
            
            # Create a page
            page = await browser.new_page()
            print("✅ New page created successfully")
            
            # Navigate to a simple page
            await page.goto('https://example.com')
            print("✅ Navigation successful")
            
            # Get page title
            title = await page.title()
            print(f"✅ Page title: {title}")
            
            # Wait a moment to see the page
            await asyncio.sleep(3)
            
            # Close browser
            await browser.close()
            print("✅ Browser closed successfully")
            
            print("🎉 All Playwright tests passed! Browser automation should work.")
            return True
            
    except Exception as e:
        print(f"❌ Playwright test failed: {e}")
        return False

async def main():
    """Main test function."""
    print("🤖 ChromeOS Playwright Browser Test")
    print("=" * 40)
    
    success = await test_playwright_launch()
    
    if success:
        print("\n✅ ChromeOS is ready for browser automation!")
        print("   You can now run the survey automation bot.")
    else:
        print("\n❌ ChromeOS browser automation test failed.")
        print("   Additional configuration may be needed.")

if __name__ == "__main__":
    asyncio.run(main())
