"""
Web Scraper and Markdown Converter
A comprehensive tool that converts web content to markdown using both HTML parsing 
and visual analysis, powered by Ell.so for intelligent content processing.
"""

import os
import logging
from typing import Optional, Dict, List
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import ell
from markdownify import markdownify as md
from dotenv import load_dotenv
import re
from bs4.element import Comment
import argparse
from PIL import Image
import io

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configure Ell logging
ell_logger = logging.getLogger('ell')
ell_logger.setLevel(logging.WARNING)  # Only show warnings and errors from Ell

# Add a custom handler for our application logs
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(message)s',
    datefmt='%H:%M:%S'
))
logger.handlers = [console_handler]

# Add progress logging in key functions
def process_url(self, url: str) -> str:
    """Process URL through three-stage conversion pipeline"""
    try:
        logger.info(f"Starting conversion for URL: {url}")
        
        # Stage 1: Visual Analysis
        logger.info("Stage 1/3: Performing visual analysis...")
        screenshot = self.visual_scraper.capture(url)
        screenshot_path = self.visual_scraper.save_screenshot(screenshot, url)
        logger.info(f"Screenshot saved to: {screenshot_path}")
        visual_analysis = analyze_page_content(Image.open(io.BytesIO(screenshot)))
        logger.info("Visual analysis complete")
        
        # Stage 2: Content Generation
        logger.info("Stage 2/3: Generating content...")
        html_content = self.html_scraper.scrape(url)
        markdown_draft = generate_markdown_draft(html_content, visual_analysis)
        logger.info("Content generation complete")
        
        # Stage 3: Markdown Validation
        logger.info("Stage 3/3: Validating markdown format...")
        final_markdown = validate_markdown_format(markdown_draft)
        logger.info("Markdown validation complete")
        
        # Save the result
        output_path = self._save_markdown(final_markdown, url)
        logger.info(f"Conversion successful! Output saved to: {output_path}")
        
        return final_markdown
        
    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        raise

class HTMLScraper:
    """Handles HTML content extraction using requests and BeautifulSoup"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def scrape(self, url: str) -> str:
        """Scrape HTML content from URL"""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"HTML scraping failed: {e}")
            raise

class VisualScraper:
    """Handles visual content capture using Selenium"""
    
    def __init__(self, output_dir: str = "output"):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.binary_location = os.getenv("CHROME_BINARY_PATH", "/usr/bin/chromium")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.output_dir = output_dir

    def save_screenshot(self, screenshot: bytes, url: str) -> str:
        """Save screenshot to output directory"""
        from urllib.parse import urlparse
        parsed = urlparse(url)
        filename = f"{parsed.netloc.split('.')[0]}_screenshot.png"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'wb') as f:
            f.write(screenshot)
        
        return filepath

    def capture(self, url: str) -> bytes:
        """Capture screenshot of the webpage"""
        try:
            self.driver.get(url)
            return self.driver.get_screenshot_as_png()
        except Exception as e:
            logger.error(f"Visual capture failed: {e}")
            raise
        finally:
            self.driver.quit()

@ell.simple(model="gpt-4o-mini")
def analyze_page_content(screenshot: Image.Image) -> Dict:
    """Analyze webpage screenshot to identify main content and structure."""
    return [
        ell.system("""You are a webpage content analyzer. Your task is to identify 
        the main content while excluding navigation, ads, and other non-essential elements.
        Focus on what a human reader would consider the primary content."""),
        ell.user([
            "Analyze this webpage screenshot and provide:",
            "1. Main content location and boundaries",
            "2. Content hierarchy (headings, sections, etc.)",
            "3. Important visual elements to preserve",
            "4. Elements to exclude (nav, ads, footers)",
            screenshot
        ])
    ]

@ell.simple(model="gpt-4o-mini")
def generate_markdown_draft(html_content: str, visual_analysis: Dict) -> str:
    """Generate initial markdown content using HTML and visual analysis results."""
    return [
        ell.system("""You are a content converter specializing in creating clean, 
        well-structured markdown. Focus only on the main content areas identified 
        in the visual analysis."""),
        ell.user(f"""
        Using this visual analysis:
        {visual_analysis}
        
        Convert the relevant parts of this HTML to markdown:
        {html_content}
        
        Follow these rules:
        1. Only include content from identified main content areas
        2. Maintain the document structure from visual analysis
        3. Preserve important visual elements noted in analysis
        4. Exclude all navigation, ads, and footer content
        5. For tables:
           - Use standard Markdown table syntax with pipes and hyphens
           - Preserve column alignment using colons in separator row
           - Maintain header rows with at least three hyphens
           - Escape pipe characters in content with backslash
           - Keep consistent column spacing for readability
        """)
    ]

@ell.simple(model="gpt-4o-mini")
def validate_markdown_format(content: str) -> str:
    """Ensure markdown content follows proper formatting rules."""
    return [
        ell.system("""You are a markdown validator that enforces strict formatting rules:
        1. For numbered lists with code blocks:
           - Add a blank line before the code block
           - Indent the code block to align with the list item's text
           - Add a blank line after the code block
           - Maintain list item numbering after code blocks
        2. For code blocks:
           - Always include language specification after backticks
           - Ensure proper indentation within lists
           - Never wrap the entire document in code fences
        3. For list items:
           - Add a blank line between major list items
           - Maintain consistent indentation for sub-items
           - Preserve numbering sequence
        4. After colons:
           - Add a line break if followed by a code block or list
           - Maintain inline if part of normal sentence
        
        IMPORTANT: Never wrap the entire document in markdown code fences. The .md file format 
        already implies markdown content."""),
        ell.user(f"""
        Format this markdown content according to the rules above:
        {content}
        
        IMPORTANT: 
        1. Output only the formatted content
        2. Start immediately with the content
        3. Do not wrap the entire document in ```markdown and ```
        4. The file should end with a new line""")
    ]

def get_markdown_rules() -> str:
    """Get markdown formatting rules from our style guide."""
    return """
    1. Headings: Use proper hierarchy (#, ##, ###, etc.) with space after #

    2. Lists: 
       Consistent bullet/number formatting with proper indentation

    3. Code blocks: 
       Always encapsulate code references within triple backticks with language specification

    4. Links: 
       Use [text](url) format consistently

    5. Images: 
       Use ![alt](url "title") format

    6. Blockquotes: 
       Use > with proper spacing

    7. Tables: 
       Align columns properly with correct cell spacing

    8. Spacing: 
       - Include blank lines between sections
       - Add line break after any colon in headers, parameters, or list definitions
       - Keep colons inline for normal sentence usage

    9. Formatting: 
       Use consistent bold/italic markers

    10. Special characters: 
        Escape when needed
    """

class MarkdownConverter:
    """Converts web content to markdown using a three-stage process:
    1. Visual Analysis
    2. Content Generation
    3. Markdown Validation
    """
    
    def __init__(self):
        self.html_scraper = HTMLScraper()
        self.visual_scraper = VisualScraper()
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)

    def process_url(self, url: str) -> str:
        """Process URL through three-stage conversion pipeline"""
        try:
            logger.info(f"Starting conversion for URL: {url}")
            
            # Stage 1: Visual Analysis
            logger.info("Stage 1/3: Performing visual analysis...")
            screenshot = self.visual_scraper.capture(url)
            screenshot_path = self.visual_scraper.save_screenshot(screenshot, url)
            logger.info(f"Screenshot saved to: {screenshot_path}")
            visual_analysis = analyze_page_content(Image.open(io.BytesIO(screenshot)))
            logger.info("Visual analysis complete")
            
            # Stage 2: Content Generation
            logger.info("Stage 2/3: Generating content...")
            html_content = self.html_scraper.scrape(url)
            markdown_draft = generate_markdown_draft(html_content, visual_analysis)
            logger.info("Content generation complete")
            
            # Stage 3: Markdown Validation
            logger.info("Stage 3/3: Validating markdown format...")
            final_markdown = validate_markdown_format(markdown_draft)
            logger.info("Markdown validation complete")
            
            # Save the result
            output_path = self._save_markdown(final_markdown, url)
            logger.info(f"Conversion successful! Output saved to: {output_path}")
            
            return final_markdown
            
        except Exception as e:
            logger.error(f"Conversion failed: {e}")
            raise

    def _save_markdown(self, markdown_content: str, url: str):
        """Save markdown content to a file"""
        filename = self._generate_filename(url)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

    def _generate_filename(self, url: str, title: str = "") -> str:
        """Generate a filename from URL or title"""
        if title:
            # Use title if available
            filename = re.sub(r'[^\w\s-]', '', title.lower())
            filename = re.sub(r'[-\s]+', '-', filename)
        else:
            # Extract just the final part of the URL path
            from urllib.parse import urlparse
            parsed = urlparse(url)
            path = parsed.path.strip('/')
            
            # Get the last component of the path
            path_parts = path.split('/')
            if path_parts:
                # Take the last part and replace dots with underscores
                filename = path_parts[-1].replace('.', '_')
            else:
                # Fallback to domain if no path
                filename = parsed.netloc.split('.')[0]
            
            # Clean up filename
            filename = re.sub(r'[^\w\s-]', '', filename)
            filename = re.sub(r'[-\s]+', '-', filename)
        
        # Ensure filename isn't too long
        if len(filename) > 50:
            filename = filename[:50]
        
        return os.path.join(self.output_dir, f"{filename}.md")

def main():
    """Main function to run the converter"""
    parser = argparse.ArgumentParser(description='Convert web content to markdown')
    parser.add_argument('--url', help='Target URL to convert')
    args = parser.parse_args()
    
    url = args.url
    if not url:
        url = input("Please enter the URL to convert to markdown: ").strip()
    
    if not url:
        logger.error("No URL provided")
        return
    
    converter = MarkdownConverter()
    try:
        markdown_content = converter.process_url(url)
        logger.info("Conversion completed successfully")
    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        raise

if __name__ == "__main__":
    main()