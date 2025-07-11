""" Crawl4AI Unit Test """
import asyncio
import tempfile
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from raglib.doc_rag.crawler import PythonDocsCrawler


@pytest.fixture
def temp_output_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


def test_crawler_initialization_valid_dir(temp_output_dir):
    crawler = PythonDocsCrawler(output_dir=temp_output_dir)
    assert crawler.output_dir.exists()
    assert crawler.output_dir.is_dir()


def test_crawler_initialization_invalid_dir():
    with pytest.raises(ValueError, match="does not exist"):
        PythonDocsCrawler(output_dir="/non/existent/path")


def test_get_urls():
    crawler = PythonDocsCrawler(output_dir=".")
    urls = crawler.get_urls()
    assert isinstance(urls, list)
    assert urls[0].startswith("https://docs.python.org")


def test_get_config():
    crawler = PythonDocsCrawler(output_dir=".")
    config = crawler.get_config()
    assert hasattr(config, "deep_crawl_strategy")
    assert hasattr(config, "scraping_strategy")
    assert config.cache_mode.name == "BYPASS"


@pytest.mark.asyncio
@patch("raglib.doc_rag.crawler.AsyncWebCrawler")
async def test_run_mocks_crawling(mock_crawler_class, temp_output_dir):
    # Mock result object with markdown
    mock_result = MagicMock()
    mock_result.markdown.raw_markdown = "# Sample Page"
    mock_crawler = AsyncMock()
    mock_crawler.__aenter__.return_value = mock_crawler
    mock_crawler.arun.return_value = [mock_result]
    mock_crawler_class.return_value = mock_crawler

    crawler = PythonDocsCrawler(output_dir=temp_output_dir)
    await crawler.run()

    # Check if a markdown file was created
    output_files = list(Path(temp_output_dir).glob("*.md"))
    assert len(output_files) == 1

    with open(output_files[0], "r", encoding="utf-8") as f:
        content = f.read()
        assert "# Sample Page" in content
