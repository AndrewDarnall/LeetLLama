""" Crawl4AI Concrete Crawler """
import asyncio
import argparse
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import List

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.deep_crawling.filters import (
    FilterChain,
    DomainFilter,
    URLPatternFilter
)
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator


class BaseCrawler(ABC):
    """
    Abstract base class for structured web crawlers using crawl4ai.
    """

    def __init__(self, output_dir: str):
        self.output_dir = Path(output_dir)

        if not output_dir:
            raise ValueError("No output directory was provided.")

        if not self.output_dir.exists() or not self.output_dir.is_dir():
            raise ValueError(f"Provided output directory '{output_dir}' does not exist or is not a valid directory.")

    @abstractmethod
    def get_urls(self) -> List[str]:
        """Return a list of URLs to crawl."""
        pass

    @abstractmethod
    def get_config(self) -> CrawlerRunConfig:
        """Return a configured CrawlerRunConfig instance."""
        pass

    async def run(self):
        """Run the crawler and write the markdown outputs."""
        urls = self.get_urls()
        config = self.get_config()

        async with AsyncWebCrawler() as crawler:
            all_results = []

            for url in urls:
                print(f"🚀 Crawling: {url}")
                results = await crawler.arun(url=url, config=config)
                all_results.extend(results)
                print(f"✅ {len(results)} page(s) scraped from {url}")

            # Save results
            for idx, result in enumerate(all_results):
                output_path = self.output_dir / f"doc_{idx}.md"
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(result.markdown.raw_markdown)

            print(f"\n📄 Total pages saved: {len(all_results)}")


class PythonDocsCrawler(BaseCrawler):
    """
    Concrete implementation of BaseCrawler for Python 3.13 reference docs.
    """

    def get_urls(self) -> List[str]:
        return ["https://docs.python.org/3.13/reference/"]

    def get_config(self) -> CrawlerRunConfig:
        filter_chain = FilterChain([
            DomainFilter(allowed_domains=["docs.python.org"]),
            URLPatternFilter(patterns=[r"^https://docs\.python\.org/3\.13/reference/"])
        ])

        return CrawlerRunConfig(
            target_elements=["body"],
            excluded_tags=["nav", "footer", "header"],
            deep_crawl_strategy=BFSDeepCrawlStrategy(
                max_depth=2,
                include_external=False,
                filter_chain=filter_chain
            ),
            scraping_strategy=LXMLWebScrapingStrategy(),
            cache_mode=CacheMode.BYPASS,
            verbose=True
        )


def parse_args():
    parser = argparse.ArgumentParser(description="PythonDocs Crawler")
    parser.add_argument(
        "--output-dir",
        type=str,
        required=True,
        help="Path to an existing directory to store markdown output."
    )
    return parser.parse_args()
