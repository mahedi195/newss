import asyncio
from crawl4ai import *

async def crawl(urls):
    async with AsyncWebCrawler() as crawler:
        final_result = []
        for url in urls:
            result = await crawler.arun(url=url)
            # Handle None markdown gracefully
            markdown_content = result.markdown if result.markdown is not None else ""
            final_result.append(markdown_content)
        return final_result

