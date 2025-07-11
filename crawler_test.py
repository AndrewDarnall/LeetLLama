import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.content_filter_strategy import PruningContentFilter, BM25ContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.deep_crawling.filters import (
    FilterChain,
    DomainFilter,
    URLPatternFilter,
    ContentTypeFilter
)



async def main():

    filter_chain = FilterChain([
        DomainFilter(
            allowed_domains=["docs.python.org"]
        ),
        URLPatternFilter(patterns=[r"^https://docs\.python\.org/3\.13/reference/"])
    ])

    crawl_config = CrawlerRunConfig(
            target_elements=["body"],
            excluded_tags=["nav", "footer", "header"],  # By tag
            # excluded_elements=["#cookie-popup", ".ads-banner", ".feedback-form"],  # By CSS selector
            deep_crawl_strategy=BFSDeepCrawlStrategy(max_depth=2, include_external=False, filter_chain=filter_chain),
            scraping_strategy=LXMLWebScrapingStrategy(),
            verbose=True,  # Show progress during crawling,
        )
    
    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun(
            url="https://docs.python.org/3.13/reference/",
            config=crawl_config
        )
        
        print(f"Total Ammount of Pages Scraped:\t{len(results)}")
    
    for idx, result in enumerate(results):
        with open(f"knowledge_base/pydoc_{idx}.md", "w") as f:
            f.write(result.markdown.raw_markdown)

if __name__ == "__main__":
    asyncio.run(main())