"""
Web Scraper and Markdown Converter
A comprehensive tool that converts web content to markdown using both HTML parsing 
and visual analysis, powered by Ell.so for intelligent content processing.

Read the README.md!
"""

import os
import logging
from typing import Optional, Dict, List, Tuple
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
import pytesseract
from .analyzer import HTMLAnalyzer
import json

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
    '%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
))
logger.handlers = [console_handler]

# Configure OpenAI client
openai_client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))

# Add progress logging in key functions
def process_url(self, url: str) -> str:
    """Process URL through conversion pipeline with OCR fallback"""
    try:
        logger.info(f"Starting conversion for URL: {url}")
        
        # Stage 1: Analysis & Strategy
        logger.info("Stage 1/3: Analyzing content...")
        analysis = self.analyzer.analyze_url(url)
        logger.info(f"Analysis complete: {analysis['recommendations']}")
        
        # Stage 2: Visual Analysis & Content Capture
        logger.info("Stage 2/3: Performing visual analysis...")
        screenshot = self.visual_scraper.capture(url)
        screenshot_path = self.visual_scraper.save_screenshot(screenshot, url)
        logger.info(f"Screenshot saved to: {screenshot_path}")
        
        # Determine processing strategy
        if analysis['processing_strategy']['use_ocr']:
            logger.info("Using OCR-based extraction...")
            image = Image.open(io.BytesIO(screenshot))
            visual_analysis = analyze_page_content(image)
            
            # Extract text using OCR
            ocr_text = pytesseract.image_to_string(image)
            markdown_draft = generate_markdown_from_ocr(ocr_text, visual_analysis)
            # Get page title from HTML for consistency
            html_content = self.html_scraper.scrape(url)
            page_title = self.html_scraper.get_page_title(html_content)
        else:
            logger.info("Using HTML-based extraction...")
            visual_analysis = analyze_page_content(Image.open(io.BytesIO(screenshot)))
            html_content = self.html_scraper.scrape(url)
            page_title = self.html_scraper.get_page_title(html_content)
            
            # Process HTML content
            html_content_chunks = filter_and_chunk_content(html_content)
            markdown_parts = []
            
            for i, chunk in enumerate(html_content_chunks, 1):
                try:
                    markdown_part = generate_markdown_draft(chunk, visual_analysis)
                    if markdown_part:
                        markdown_parts.append(markdown_part)
                except openai.BadRequestError as e:
                    if "context_length_exceeded" in str(e):
                        smaller_chunks = filter_and_chunk_content(chunk, max_chunk_size=50000)
                        for smaller_chunk in smaller_chunks:
                            markdown_part = generate_markdown_draft(smaller_chunk, visual_analysis)
                            if markdown_part:
                                markdown_parts.append(markdown_part)
                    else:
                        raise e
            
            markdown_draft = '\n\n'.join(filter(None, markdown_parts))
        
        # Stage 3: Markdown Validation
        logger.info("Stage 3/3: Validating markdown format...")
        final_markdown = validate_markdown_format(markdown_draft)
        final_markdown = validate_document_title(final_markdown, visual_analysis, page_title)
        
        # Remove the save operation from here since it's handled in process_urls_from_config
        return final_markdown
        
    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        raise

def filter_and_chunk_content(content: str, max_chunk_size: int = 100000) -> List[str]:
    """Filter JSX/React components and split content into chunks"""
    # First filter out unnecessary content
    filtered_content = re.sub(r'<script\b[^>]*>[\s\S]*?</script>', '', content)
    filtered_content = re.sub(r'_jsx\([^)]+\)|_jsxs\([^)]+\)', '', filtered_content)
    filtered_content = re.sub(r'className="[^"]*"', '', filtered_content)
    filtered_content = re.sub(r'children=\{[^}]*\}', '', filtered_content)
    
    # Then split into chunks using existing logic
    sections = re.split(r'\n(?=# |\## |\### )', filtered_content)
    chunks = []
    current_chunk = []
    current_size = 0
    
    for section in sections:
        section_size = len(section) // 4
        if current_size + section_size > max_chunk_size and current_chunk:
            chunks.append('\n'.join(current_chunk))
            current_chunk = []
            current_size = 0
        current_chunk.append(section)
        current_size += section_size
    
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
def generate_markdown_from_ocr(ocr_text: str, visual_analysis: Dict) -> str:
    """Convert OCR-extracted text to markdown using visual analysis for structure"""
    return [
        ell.system("""You are a documentation converter specializing in API documentation. 
        Convert OCR-extracted text to clean, structured markdown while preserving:
        1. Code blocks (maintain language-specific syntax)
        2. Parameter descriptions and types
        3. Visual hierarchy from the analysis
        4. Tables and lists
        """),
        ell.user(f"""Using this visual structure analysis:
        {json.dumps(visual_analysis, indent=2)}
        
        Convert this OCR-extracted text to markdown, ensuring proper formatting:
        {ocr_text}
        
        Follow these guidelines:
        1. Use proper markdown heading levels (# ## ###) based on visual_analysis hierarchy
        2. Format code blocks with ```language_name
        3. Preserve parameter types and descriptions in consistent format
        4. Maintain proper spacing between sections
        5. Clean up any OCR artifacts or misalignments
        """)
    ]

@ell.simple(model="gpt-4o-mini", client=openai_client)
def generate_markdown_draft(html_content: str, visual_analysis: Dict) -> str:
    """Generate initial markdown content using HTML and visual analysis results."""
    return [
        ell.system("""You are a content converter specializing in creating clean, 
        well-structured markdown. Focus only on the main content areas identified 
        in the visual analysis. Follow these line break rules strictly:
        1. Single line break after each heading
        2. No extra line breaks between list items
        3. Single line break between different sections
        4. No multiple consecutive line breaks
        5. Single line break at end of document"""),
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
        5. For line breaks:
           - Single break after headings
           - No breaks between list items
           - Single break between sections
           - No consecutive breaks
        6. For lists:
           - No extra breaks between items
           - Single break before and after list
        7. For tables, links, references, and images:
           [Previous rules remain the same...]
        """)
    ]

@ell.simple(model="gpt-4o-mini", client=openai_client)
def validate_markdown_format(content: str) -> str:
    """Ensure markdown content follows proper formatting rules."""
    # First clean up multiple line breaks
    content = re.sub(r'\n{3,}', '\n\n', content)  # Replace 3+ newlines with 2
    content = re.sub(r'\n+$', '\n', content)      # Single newline at end
    
    # Apply specific validation functions
    content = validate_table_format(content)
    content = validate_list_format(content)
    content = validate_code_blocks(content)
    
    return [
        ell.system("""You are a markdown validator that enforces strict formatting rules:
        1. Line breaks:
           - Single break after headings
           - No breaks between list items
           - Single break between sections
           - Remove consecutive breaks
           - Single break at end of file
        2. For lists:
           - Remove extra breaks between items
           - Single break before and after list
        3. For code blocks:
           - Single break before and after
           - Include language specification
        4. After colons:
           - No extra breaks unless followed by list/code
        
        IMPORTANT: Never add unnecessary line breaks. The document should be compact 
        but readable."""),
        ell.user(f"""
        Format this pre-validated markdown content according to the rules above:
        {content}
        
        IMPORTANT: 
        1. Output only the formatted content
        2. Start immediately with the content
        3. Do not wrap in markdown fences
        4. Single newline at end""")
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

class ContentProcessor:
    """Handles content processing with OCR and visual analysis capabilities"""
    
    def __init__(self):
        self.html_scraper = HTMLScraper()
        self.visual_scraper = VisualScraper()
        self.analyzer = HTMLAnalyzer()
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)

    def process_url(self, url: str) -> str:
        """Process URL through conversion pipeline with OCR fallback"""
        try:
            logger.info(f"Starting conversion for URL: {url}")
            
            # Stage 1: Analysis & Strategy
            logger.info("Stage 1/3: Analyzing content...")
            analysis = self.analyzer.analyze_url(url)
            logger.info(f"Analysis complete: {analysis['recommendations']}")
            
            # Stage 2: Visual Analysis & Content Capture
            logger.info("Stage 2/3: Performing visual analysis...")
            screenshot = self.visual_scraper.capture(url)
            screenshot_path = self.visual_scraper.save_screenshot(screenshot, url)
            logger.info(f"Screenshot saved to: {screenshot_path}")
            
            # Determine processing strategy
            if analysis['processing_strategy']['use_ocr']:
                logger.info("Using OCR-based extraction...")
                image = Image.open(io.BytesIO(screenshot))
                visual_analysis = analyze_page_content(image)
                
                # Extract text using OCR
                ocr_text = pytesseract.image_to_string(image)
                markdown_draft = generate_markdown_from_ocr(ocr_text, visual_analysis)
                # Get page title from HTML for consistency
                html_content = self.html_scraper.scrape(url)
                page_title = self.html_scraper.get_page_title(html_content)
            else:
                logger.info("Using HTML-based extraction...")
                visual_analysis = analyze_page_content(Image.open(io.BytesIO(screenshot)))
                html_content = self.html_scraper.scrape(url)
                page_title = self.html_scraper.get_page_title(html_content)
                
                # Process HTML content
                html_content_chunks = filter_and_chunk_content(html_content)
                markdown_parts = []
                
                for i, chunk in enumerate(html_content_chunks, 1):
                    try:
                        markdown_part = generate_markdown_draft(chunk, visual_analysis)
                        if markdown_part:
                            markdown_parts.append(markdown_part)
                    except openai.BadRequestError as e:
                        if "context_length_exceeded" in str(e):
                            smaller_chunks = filter_and_chunk_content(chunk, max_chunk_size=50000)
                            for smaller_chunk in smaller_chunks:
                                markdown_part = generate_markdown_draft(smaller_chunk, visual_analysis)
                                if markdown_part:
                                    markdown_parts.append(markdown_part)
                        else:
                            raise e
                
                markdown_draft = '\n\n'.join(filter(None, markdown_parts))
            
            # Stage 3: Markdown Validation
            logger.info("Stage 3/3: Validating markdown format...")
            final_markdown = validate_markdown_format(markdown_draft)
            final_markdown = validate_document_title(final_markdown, visual_analysis, page_title)
            
            # Remove the save operation from here since it's handled in process_urls_from_config
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
        filename = f"{prefix}-{sequence:03d}-{clean_segment}"
        
        # Truncate if too long (leaving room for extension)
        if len(filename) > 46:  # 50 - 4 (.md)
            filename = filename[:46]
        
        return os.path.join(self.output_dir, f"{filename}.md")

    def process_urls_from_config(self, config_file: str, prefix: str = "doc") -> List[str]:
        """Process multiple URLs from a config file with retry logic"""
        logger.info(f"Reading URLs from config file: {config_file}")
        
        try:
            # Use the new parser
            url_entries = parse_config_file(config_file)
            
            if not url_entries:
                raise ValueError("No valid URLs found in config file")
            
            output_files = []
            failed_urls = []
            
            for number, url in url_entries:
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        logger.info(f"Processing URL {number}/{len(url_entries)}: {url} (attempt {attempt + 1}/{max_retries})")
                        markdown_content = self.process_url(url)
                        
                        # Use the number from the config file instead of the loop index
                        output_file = self._generate_sequence_filename(url, prefix, number)
                        with open(output_file, 'w', encoding='utf-8') as f:
                            f.write(markdown_content)
                        
                        output_files.append(output_file)
                        logger.info(f"Saved to: {output_file}")
                        break
                        
                    except Exception as e:
                        logger.error(f"Attempt {attempt + 1} failed for URL {number}, {url}: {e}")
                        if attempt == max_retries - 1:
                            failed_urls.append((number, url))
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
    """Ensure proper list formatting without extra breaks"""
    lines = content.split('\n')
    result = []
    in_list = False
    prev_was_list = False
    
    for line in lines:
        is_list_item = bool(re.match(r'^[*+-]|\d+\.', line.strip()))
        
        if is_list_item:
            if not in_list and not prev_was_list:
                result.append('')  # Single break before list starts
            in_list = True
        else:
            if in_list and line.strip():  # Non-empty non-list line
                result.append('')  # Single break after list ends
            in_list = False
        
        result.append(line)
        prev_was_list = is_list_item
    
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

def filter_jsx_content(html_content: str) -> str:
    """
    Filter out unnecessary JSX/React components from HTML content
    """
    import re
    
    # Remove script tags and their contents
    html_content = re.sub(r'<script\b[^>]*>[\s\S]*?</script>', '', html_content)
    
    # Remove JSX component syntax
    html_content = re.sub(r'_jsx\([^)]+\)', '', html_content)
    html_content = re.sub(r'_jsxs\([^)]+\)', '', html_content)
    
    # Remove React-specific attributes
    html_content = re.sub(r'className="[^"]*"', '', html_content)
    html_content = re.sub(r'children=\{[^}]*\}', '', html_content)
    
    # Remove component definitions
    html_content = re.sub(r'function \w+\([^)]*\)\s*\{[\s\S]*?\}', '', html_content)
    
    # Remove object assignments
    html_content = re.sub(r'const \{[^}]*\} = [^;]*;', '', html_content)
    
    # Clean up multiple newlines and spaces
    html_content = re.sub(r'\n\s*\n', '\n\n', html_content)
    html_content = re.sub(r' +', ' ', html_content)
    
    return html_content.strip()

def parse_config_file(config_path: str) -> List[Tuple[int, str]]:
    """
    Parse the config file containing numbered URLs
    Returns a list of tuples containing (number, url)
    """
    urls = []
    with open(config_path, 'r') as f:
        yaml_content = yaml.safe_load(f)
        
        if 'urls' in yaml_content:
            for url_entry in yaml_content['urls']:
                # Split on comma and strip whitespace
                parts = url_entry.split(',', 1)
                if len(parts) == 2:
                    # Extract number and URL
                    number = int(parts[0].strip())
                    url = parts[1].strip()
                    urls.append((number, url))
    
    # Sort by number to maintain order
    urls.sort(key=lambda x: x[0])
    return urls

def main():
    """Main function to run the converter"""
    parser = argparse.ArgumentParser(description='Convert web content to markdown')
    parser.add_argument('--url', help='Target URL to convert')
    parser.add_argument('--config', help='YAML config file containing URLs to process')
    parser.add_argument('--prefix', default='doc', help='Prefix for output filenames (default: doc)')
    args = parser.parse_args()
    
    converter = ContentProcessor()
    
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