"""
Web Scraper and Markdown Converter
A comprehensive tool that converts web content to markdown using both HTML parsing 
and visual analysis, powered by Ell.so for intelligent content processing.

Read the README.md!
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
import openai
import base64
import yaml
from urllib.parse import urlparse
import time

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
ell_logger.setLevel(logging.WARNING)  
ell.init(verbose=True, store='./logs', autocommit=True)

# Add a custom handler for our application logs
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(message)s',
    datefmt='%H:%M:%S'
))
logger.handlers = [console_handler]

# Configure OpenAI client
openai_client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))

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
        page_title = self.html_scraper.get_page_title(html_content)
        
        # Split content into chunks and process each chunk
        html_content_chunks = chunk_content(html_content)
        markdown_parts = []
        logger.info(f"Split content into {len(html_content_chunks)} chunks")
        
        for i, chunk in enumerate(html_content_chunks, 1):
            try:
                logger.info(f"Processing chunk {i}/{len(html_content_chunks)}")
                markdown_part = generate_markdown_draft(chunk, visual_analysis)
                if markdown_part:
                    markdown_parts.append(markdown_part)
                else:
                    logger.warning(f"Empty result from chunk {i}")
            except openai.BadRequestError as e:
                if "context_length_exceeded" in str(e):
                    logger.warning(f"Chunk {i} too large, splitting further...")
                    smaller_chunks = chunk_content(chunk, max_chunk_size=50000)
                    for j, smaller_chunk in enumerate(smaller_chunks, 1):
                        logger.info(f"Processing sub-chunk {j}/{len(smaller_chunks)} of chunk {i}")
                        markdown_part = generate_markdown_draft(smaller_chunk, visual_analysis)
                        if markdown_part:
                            markdown_parts.append(markdown_part)
                else:
                    raise e
        
        # Join chunks with double newlines to ensure proper separation
        markdown_draft = '\n\n'.join(filter(None, markdown_parts))
        logger.info(f"Combined {len(markdown_parts)} parts into final document")
        logger.info("Content generation complete")
        
        # Stage 3: Markdown Validation
        logger.info("Stage 3/3: Validating markdown format...")
        final_markdown = validate_markdown_format(markdown_draft)
        final_markdown = validate_document_title(final_markdown, visual_analysis, page_title)
        logger.info("Markdown validation complete")
        
        # Save the result
        output_path = self._save_markdown(final_markdown, url)
        logger.info(f"Conversion successful! Output saved to: {output_path}")
        
        return final_markdown
        
    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        raise

def chunk_content(content: str, max_chunk_size: int = 100000) -> List[str]:
    """Split content into smaller chunks to avoid token limits"""
    # Split content at major section boundaries
    sections = re.split(r'\n(?=# |\## |\### )', content)
    chunks = []
    current_chunk = []
    current_size = 0
    
    for section in sections:
        # Rough estimate of tokens (characters / 4)
        section_size = len(section) // 4
        
        # If adding this section would exceed max size, start new chunk
        if current_size + section_size > max_chunk_size and current_chunk:
            chunks.append('\n'.join(current_chunk))
            current_chunk = []
            current_size = 0
            
        # Add section to current chunk
        current_chunk.append(section)
        current_size += section_size
    
    # Don't forget the last chunk
    if current_chunk:
        chunks.append('\n'.join(current_chunk))
    
    return chunks

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

    def get_page_title(self, html_content: str) -> str:
        """Extract page title from HTML content"""
        soup = BeautifulSoup(html_content, 'html.parser')
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.string.strip()
        return None

class VisualScraper:
    """Handles visual content capture using Selenium"""
    
    def __init__(self, max_retries=3, output_dir="output"):
        self.driver = None
        self.max_retries = max_retries
        self.output_dir = output_dir
    
    def _ensure_driver(self):
        """Ensure we have a working WebDriver instance"""
        try:
            if self.driver:
                try:
                    # Test if driver is responsive
                    self.driver.current_url
                    return
                except:
                    logger.warning("Existing WebDriver unresponsive, recreating...")
                    self._quit_driver()
            
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            self.driver = webdriver.Chrome(options=options)
            logger.info("New WebDriver instance created")
            
        except Exception as e:
            logger.error(f"Failed to create WebDriver: {e}")
            raise
    
    def _quit_driver(self):
        """Safely quit the WebDriver"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
    
    def capture(self, url):
        """Capture screenshot with retries"""
        for attempt in range(self.max_retries):
            try:
                self._ensure_driver()
                self.driver.get(url)
                time.sleep(2)  # Wait for page load
                return self.driver.get_screenshot_as_png()
                
            except Exception as e:
                logger.warning(f"Screenshot attempt {attempt + 1} failed: {e}")
                self._quit_driver()
                if attempt == self.max_retries - 1:
                    raise
                time.sleep(1)  # Wait before retry
    
    def __del__(self):
        self._quit_driver()
    
    def save_screenshot(self, screenshot_data: bytes, url: str) -> str:
        """Save screenshot to file and return the path"""
        # Create screenshots directory if it doesn't exist
        screenshots_dir = os.path.join(self.output_dir, 'screenshots')
        os.makedirs(screenshots_dir, exist_ok=True)
        
        # Generate filename from URL
        filename = re.sub(r'[^\w\s-]', '', urlparse(url).path.strip('/').replace('/', '-'))
        if not filename:
            filename = 'homepage'
        
        # Add timestamp to ensure uniqueness
        timestamp = time.strftime('%Y%m%d-%H%M%S')
        filepath = os.path.join(screenshots_dir, f'{filename}-{timestamp}.png')
        
        # Save the screenshot
        with open(filepath, 'wb') as f:
            f.write(screenshot_data)
        
        return filepath

def split_content(screenshot):
    """
    Split the screenshot into logical sections for analysis
    
    Args:
        screenshot: PIL Image object of the webpage
        
    Returns:
        List of section images
    """
    # Basic implementation - can be enhanced based on needs
    return [screenshot]  # For now, return full screenshot as single section

@ell.simple(model="gpt-4o-mini", client=openai_client)
def analyze_page_content(screenshot: Image.Image) -> Dict:
    """Analyze webpage screenshot to identify main content and structure."""
    # Convert to RGB if image is in RGBA mode
    if screenshot.mode == 'RGBA':
        screenshot = screenshot.convert('RGB')
    
    # Progressive optimization steps
    max_size = (800, 800)  # Reduced from 1024x1024
    screenshot.thumbnail(max_size, Image.Resampling.LANCZOS)
    
    return [
        ell.system("""You are a webpage content analyzer. Analyze the screenshot and provide a structured analysis in the following JSON format:
        {
            "main_content": {
                "top": float,    // Relative position from top (0-1)
                "bottom": float, // Relative position from bottom (0-1)
                "left": float,   // Relative position from left (0-1)
                "right": float   // Relative position from right (0-1)
            },
            "hierarchy": [       // List of content sections in order
                {
                    "type": "heading|paragraph|list|table|code",
                    "level": int,
                    "position": float  // Relative position from top (0-1)
                }
            ],
            "visual_elements": [ // Important visual elements to preserve
                {
                    "type": "image|table|code|blockquote",
                    "position": float,
                    "importance": 1-5
                }
            ],
            "exclude": [        // Areas to exclude from conversion
                {
                    "type": "navigation|sidebar|footer|ad",
                    "position": float
                }
            ]
        }"""),
        ell.user(["Analyze this webpage screenshot and provide the structured analysis.", screenshot])
    ]

@ell.simple(model="gpt-4o-mini", client=openai_client)
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
        6. For links:
           - Preserve all hyperlinks using [text](url) format
           - Keep reference-style links at the bottom of sections
           - Maintain link text formatting (bold, italic) inside brackets
           - For external links, use absolute URLs
           - For internal links, use relative paths
        7. For references and citations:
           - Preserve footnote links using [^n] format
           - Keep citation links in reference-style format
           - Maintain original link text and URLs
        8. For images:
           - Include important images identified in visual analysis
           - Use standard markdown image syntax: ![alt text](image url)           
           - Link to the images using their original URLs
        """)
    ]

@ell.simple(model="gpt-4o-mini", client=openai_client)
def validate_markdown_format(content: str) -> str:
    """Ensure markdown content follows proper formatting rules."""
    # First apply our specific validation functions
    content = validate_table_format(content)
    content = validate_list_format(content)
    content = validate_code_blocks(content)
    
    # Then use Ell.so for additional validation and formatting
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
        Format this pre-validated markdown content according to the rules above:
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
            page_title = self.html_scraper.get_page_title(html_content)
            
            # Split content into chunks and process each chunk
            html_content_chunks = chunk_content(html_content)
            markdown_parts = []
            logger.info(f"Split content into {len(html_content_chunks)} chunks")
            
            for i, chunk in enumerate(html_content_chunks, 1):
                try:
                    logger.info(f"Processing chunk {i}/{len(html_content_chunks)}")
                    markdown_part = generate_markdown_draft(chunk, visual_analysis)
                    if markdown_part:
                        markdown_parts.append(markdown_part)
                    else:
                        logger.warning(f"Empty result from chunk {i}")
                except openai.BadRequestError as e:
                    if "context_length_exceeded" in str(e):
                        logger.warning(f"Chunk {i} too large, splitting further...")
                        smaller_chunks = chunk_content(chunk, max_chunk_size=50000)
                        for j, smaller_chunk in enumerate(smaller_chunks, 1):
                            logger.info(f"Processing sub-chunk {j}/{len(smaller_chunks)} of chunk {i}")
                            markdown_part = generate_markdown_draft(smaller_chunk, visual_analysis)
                            if markdown_part:
                                markdown_parts.append(markdown_part)
                    else:
                        raise e
            
            # Join chunks with double newlines to ensure proper separation
            markdown_draft = '\n\n'.join(filter(None, markdown_parts))
            logger.info(f"Combined {len(markdown_parts)} parts into final document")
            logger.info("Content generation complete")
            
            # Stage 3: Markdown Validation
            logger.info("Stage 3/3: Validating markdown format...")
            final_markdown = validate_markdown_format(markdown_draft)
            final_markdown = validate_document_title(final_markdown, visual_analysis, page_title)
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

    def _generate_sequence_filename(self, url: str, prefix: str, sequence: int) -> str:
        """Generate a filename with sequence number and prefix"""
        # Extract the last part of the path
        path = urlparse(url).path.strip('/')
        last_segment = path.split('/')[-1] if path else ''
        
        # Clean up the segment
        clean_segment = re.sub(r'[^\w\s-]', '', last_segment.lower())
        clean_segment = re.sub(r'[-\s]+', '-', clean_segment)
        
        # Format with two-digit sequence number
        filename = f"{prefix}-{sequence:02d}-{clean_segment}"
        
        # Truncate if too long (leaving room for extension)
        if len(filename) > 46:  # 50 - 4 (.md)
            filename = filename[:46]
        
        return os.path.join(self.output_dir, f"{filename}.md")

    def process_urls_from_config(self, config_file: str, prefix: str = "doc") -> List[str]:
        """Process multiple URLs from a config file with retry logic"""
        logger.info(f"Reading URLs from config file: {config_file}")
        
        try:
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
            
            if not config or 'urls' not in config:
                raise ValueError("Config file must contain a 'urls' list")
            
            output_files = []
            failed_urls = []
            
            for i, url in enumerate(config['urls'], 1):
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        logger.info(f"Processing URL {i}/{len(config['urls'])}: {url} (attempt {attempt + 1}/{max_retries})")
                        markdown_content = self.process_url(url)
                        
                        output_file = self._generate_sequence_filename(url, prefix, i)
                        with open(output_file, 'w', encoding='utf-8') as f:
                            f.write(markdown_content)
                        
                        output_files.append(output_file)
                        logger.info(f"Saved to: {output_file}")
                        break
                        
                    except Exception as e:
                        logger.error(f"Attempt {attempt + 1} failed for URL {url}: {e}")
                        if attempt == max_retries - 1:
                            failed_urls.append(url)
                        time.sleep(2)  # Wait before retry
            
            if failed_urls:
                logger.error(f"Failed to process {len(failed_urls)} URLs: {failed_urls}")
            
            logger.info(f"Batch processing completed. Generated {len(output_files)} files")
            return output_files
            
        except Exception as e:
            logger.error(f"Error reading config file: {e}")
            raise

@ell.simple(model="gpt-4o-mini", client=openai_client)
def analyze_section(section: Image.Image) -> Dict:
    """Analyze a single section of the webpage screenshot."""
    # Resize section if needed
    max_size = (1024, 1024)
    section.thumbnail(max_size, Image.Resampling.LANCZOS)
    
    return [
        ell.system("""You are a webpage section analyzer. Analyze this section and provide structured analysis in the same JSON format as the main analyzer."""),
        ell.user(["Analyze this section of the webpage and provide structured analysis.", section])
    ]

def combine_results(results: List[Dict]) -> Dict:
    """Combine multiple section analysis results into a single analysis."""
    combined = {
        "main_content": {"top": float('inf'), "bottom": 0, "left": float('inf'), "right": 0},
        "hierarchy": [],
        "visual_elements": [],
        "exclude": []
    }
    
    for result in results:
        # Update main content boundaries
        combined["main_content"]["top"] = min(combined["main_content"]["top"], result["main_content"]["top"])
        combined["main_content"]["bottom"] = max(combined["main_content"]["bottom"], result["main_content"]["bottom"])
        combined["main_content"]["left"] = min(combined["main_content"]["left"], result["main_content"]["left"])
        combined["main_content"]["right"] = max(combined["main_content"]["right"], result["main_content"]["right"])
        
        # Combine other elements
        combined["hierarchy"].extend(result["hierarchy"])
        combined["visual_elements"].extend(result["visual_elements"])
        combined["exclude"].extend(result["exclude"])
    
    return combined

def validate_table_format(table_content: str) -> str:
    """Ensure table formatting follows markdown standards"""
    lines = table_content.split('\n')
    if len(lines) >= 2:
        # Add alignment indicators in separator row
        header_cells = lines[0].count('|') - 1
        separator = '|' + '|'.join([':---:|' for _ in range(header_cells)])
        lines[1] = separator
    return '\n'.join(lines)

def validate_list_format(content: str) -> str:
    """Ensure proper list formatting"""
    lines = content.split('\n')
    result = []
    in_list = False
    
    for line in lines:
        if re.match(r'^[*+-]|\d+\.', line.strip()):
            if not in_list:
                result.append('')  # Add blank line before list
            in_list = True
        elif line.strip() == '':
            in_list = False
        result.append(line)
    
    return '\n'.join(result)

def validate_code_blocks(content: str) -> str:
    """Ensure code blocks have language specification"""
    pattern = r'```\s*\n'  # Find code blocks without language
    replacement = '```text\n'  # Default to text if no language specified
    return re.sub(pattern, replacement, content)

def validate_html_structure(html_content: str) -> str:
    """Validate HTML structure and clean invalid markup."""
    pass

def validate_content_relevance(html_content: str, visual_analysis: Dict) -> str:
    """Validate content relevance against visual analysis."""
    pass

def validate_html_elements(html_content: str) -> str:
    """Validate specific HTML elements for conversion."""
    pass

def validate_heading_hierarchy(content: str) -> str:
    """Validate heading levels and structure."""
    pass

def validate_link_formatting(content: str) -> str:
    """Validate link syntax and references."""
    pass

def validate_image_formatting(content: str) -> str:
    """Validate image syntax and references."""
    pass

def validate_chunk_size(chunk: str, max_size: int) -> bool:
    """Validate chunk size against token limits."""
    pass

def validate_chunk_boundaries(chunk: str) -> bool:
    """Validate chunk split points at logical boundaries."""
    pass

def validate_chunk_context(chunk: str, surrounding_chunks: List[str]) -> bool:
    """Validate chunk context preservation."""
    pass

def validate_document_title(content: str, visual_analysis: Dict, page_title: Optional[str] = None) -> str:
    """Ensure document has proper title formatting."""
    # Check if content starts with a level 1 heading
    if not content.startswith('# '):
        if page_title:
            content = f'# {page_title}\n\n{content}'
        elif 'title' in visual_analysis:
            title = visual_analysis['title']
            content = f'# {title}\n\n{content}'
        else:
            # Fallback to extracting title from first visible heading
            first_heading = visual_analysis.get('hierarchy', [])[0]
            if first_heading:
                content = f'# {first_heading["text"]}\n\n{content}'
    return content

def main():
    """Main function to run the converter"""
    parser = argparse.ArgumentParser(description='Convert web content to markdown')
    parser.add_argument('--url', help='Target URL to convert')
    parser.add_argument('--config', help='YAML config file containing URLs to process')
    parser.add_argument('--prefix', default='doc', help='Prefix for output filenames (default: doc)')
    args = parser.parse_args()
    
    converter = MarkdownConverter()
    
    try:
        if args.config:
            # Batch processing mode
            output_files = converter.process_urls_from_config(args.config, args.prefix)
            logger.info(f"Batch processing completed. Generated {len(output_files)} files")
            
        else:
            # Single URL mode
            url = args.url or input("Please enter the URL to convert to markdown: ").strip()
            if not url:
                logger.error("No URL provided")
                return
                
            markdown_content = converter.process_url(url)
            logger.info("Conversion completed successfully")
    
    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        raise

if __name__ == "__main__":
    main()