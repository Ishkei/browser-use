#!/usr/bin/env python3
"""
Headless Playwright test for ChromeOS - optimized for automation
"""

import asyncio
from playwright.async_api import async_playwright

async def test_headless_browser():
    """Test headless browser launch on ChromeOS."""
    
    print("🧪 Testing headless browser launch on ChromeOS...")
    
    try:
        async with async_playwright() as p:
            print("✅ Playwright context created successfully")
            
            # Try to launch Chromium with ChromeOS-optimized arguments
            browser = await p.chromium.launch(
                headless=True,
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
            print("✅ Headless Chromium browser launched successfully")
            
            # Create a page
            page = await browser.new_page()
            print("✅ New page created successfully")
            
            # Navigate to a simple page
            await page.goto('https://example.com')
            print("✅ Navigation successful")
            
            # Get page title
            title = await page.title()
            print(f"✅ Page title: {title}")
            
            # Try to get page content
            content = await page.text_content('body')
            if content and len(content) > 0:
                print("✅ Page content retrieved successfully")
            else:
                print("⚠️ Page content retrieval may have issues")
            
            # Close browser
            await browser.close()
            print("✅ Browser closed successfully")
            
            print("🎉 Headless browser automation works on ChromeOS!")
            return True
            
    except Exception as e:
        print(f"❌ Headless browser test failed: {e}")
        return False

async def test_basic_automation():
    """Test basic automation features."""
    
    print("\n🧪 Testing basic automation features...")
    
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--disable-software-rasterizer',
                ]
            )
            
            page = await browser.new_page()
            
            # Test form filling
            await page.goto('data:text/html,<html><body><input type="text" id="test-input"><button id="test-button">Click</button></body></html>')
            await page.fill('#test-input', 'Test automation')
            await page.click('#test-button')
            print("✅ Form filling and clicking works")
            
            # Test waiting and element detection
            await page.goto('data:text/html,<html><body><div id="content">Survey content</div></body></html>')
            element = page.locator('#content')
            text = await element.text_content()
            if text == 'Survey content':
                print("✅ Element detection and text extraction works")
            
            await browser.close()
            return True
            
    except Exception as e:
        print(f"❌ Basic automation test failed: {e}")
        return False

async def main():
    """Main test function."""
    print("🤖 ChromeOS Headless Browser Automation Test")
    print("=" * 50)
    
    # Test headless browser
    headless_success = await test_headless_browser()
    
    # Test basic automation
    automation_success = await test_basic_automation()
    
    if headless_success and automation_success:
        print("\n🎉 SUCCESS! ChromeOS can run headless browser automation!")
        print("✅ Your survey automation bot should work in headless mode.")
        print("\n🚀 Next steps:")
        print("   1. Run: python3 survey_automation.py")
        print("   2. Or: python3 run_local.py")
        print("   3. Make sure to set headless=True in the browser profile")
    else:
        print("\n❌ ChromeOS browser automation needs additional configuration.")
        print("💡 Try running with Docker or cloud-based automation.")

if __name__ == "__main__":
    asyncio.run(main())
