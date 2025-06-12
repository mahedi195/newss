

import asyncio
from crawl4ai import *

async def crawl(urls):
    async with AsyncWebCrawler() as crawler:
        # Create coroutine tasks for all URLs
        tasks = [crawler.arun(url=url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        final_result = []
        for result in results:
            if isinstance(result, Exception):
                # Handle error, optionally log it (you can also log the specific exception here)
                final_result.append("")
            else:
                markdown_content = result.markdown if result.markdown is not None else ""
                final_result.append(markdown_content)

        return final_result
