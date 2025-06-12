import subprocess
import sys
import time
import schedule
import asyncio
import logging
import os
from datetime import datetime
from crawler import crawl
from gemini import generate


def install_playwright_browsers():
    subprocess.run([sys.executable, "-m", "playwright", "install"], check=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("crawler_bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Centralized list of news websites to crawl
news_urls = [
    "https://thedailystar.net",
    "https://prothomalo.com",
    "https://bdnews24.com",
    "https://jugantor.com",
    "https://banglatribune.com",
    "https://www.bd-pratidin.com/",
    "https://ittefaq.com.bd",
    "https://www.dailyamardesh.com/",
    "https://manobkantha.com",
    "https://samakal.com",
    "https://kalerkantho.com",
    "https://www.facebook.com/dbcnews.tv/",
    "https://www.facebook.com/ekattor.tv/",
    "https://www.facebook.com/ntvdigital/",
]

def crawl_job():
    """Run the crawler and save the results to a file with timestamp"""
    logger.info("Starting scheduled crawl job")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    try:
        # Handle event loop safely (works in Streamlit or scripts)
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        result = loop.run_until_complete(crawl(urls=news_urls))

        # Create news directory if it doesn't exist
        news_dir = os.path.join(os.path.dirname(__file__), "news")
        os.makedirs(news_dir, exist_ok=True)

        # Save results to a timestamped file
        filename = os.path.join(news_dir, f"news_{timestamp}.md")
        with open(filename, "w", encoding="utf-8") as f:
            for r in result:
                f.write(r)
                f.write("\n")

        logger.info(f"Crawl completed successfully. Results saved to {filename}")
    except Exception as e:
        logger.error(f"Error during crawl: {str(e)}")

def run_bot():
    """Set up the scheduler and run indefinitely"""
    logger.info("News crawler bot started")

    # Schedule the job to run every 24 hours
    schedule.every(24).hours.do(crawl_job)

    # Run the job once at startup
    crawl_job()

    # Continuously run scheduled jobs
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    try:
        install_playwright_browsers()  # Install Playwright browsers before running bot
        run_bot()
    except KeyboardInterrupt:
        logger.info("Bot stopped manually by user.")
