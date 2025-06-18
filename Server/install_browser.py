import asyncio
from pyppeteer import launch

async def main():
    browser = await launch(headless=True)
    await browser.close()
    print("✅ Chromium installed and launched successfully!")

asyncio.run(main())