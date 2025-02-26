import asyncio
import random
from playwright.async_api import async_playwright

async def access_page():
    username = f"user{random.randint(0, 10000000)}"  # Random username for Tor isolation
    async with async_playwright() as p:
        browser = await p.firefox.launch(
            proxy={
                "server": "socks5://localhost:9050",
                "username": username,
                "password": ""  # No password needed
            }
        )
        context = await browser.new_context()
        page = await context.new_page()
        try:
            await page.goto(
                "https://www.browserling.com/browse/win10/chrome127/http://testingimp.great-site.net",
                timeout=120000
            )
            print(f"Accessing with username: {username}")
            await page.wait_for_timeout(180000)  # Wait 3 minutes
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

async def worker():
    while True:
        await access_page()

async def main():
    # Start 5 parallel workers
    tasks = [worker() for _ in range(5)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
