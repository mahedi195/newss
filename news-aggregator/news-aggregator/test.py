'''
from crawler import crawl
from gemini import generate
import asyncio

news_urls = [
    "https://thedailystar.net",
    "https://prothomalo.com",
    # "https://bdnews24.com",
    # "https://jugantor.com",
    # "https://banglatribune.com",
    # "https://banglanews24.com",
    # "https://ittefaq.com.bd",
    # "https://dailynayadiganta.com",
    # "https://manobkantha.com",
    # "https://samakal.com",
    # "https://kalerkantho.com",
]

async def main():
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(crawl())
    
    summary = generate(contents=["summerize the news and give short summary what is happening in bangladesh:   ", result])
    print(summary)    



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(crawl(news_urls))
    # print(result)
    summary = generate(contents=f"summerize the news and give short summary what is happening in bangladesh: {result}")
    print(summary)    
    # asyncio.run(main())'''