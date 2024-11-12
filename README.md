# Web to Markdown Converter

## Author: [Jon Pappas](https://github.com/matt-rickard)

A powerful Python-based tool that converts web content into well-formatted Markdown by combining HTML parsing and visual analysis, powered by Ell.so for intelligent content processing.

## Features

- Intelligent content extraction using visual analysis
- HTML parsing with BeautifulSoup
- Visual capture using Selenium
- GPT-4 Vision powered content analysis
- Clean Markdown formatting with customizable rules
- Docker containerization for easy deployment
- Comprehensive error handling and logging
- Progress tracking for conversion stages

## Prerequisites

- Python 3.11 or higher
- Docker and Docker Compose
- Chrome/Chromium browser (for Selenium)
- Ell.so API access

## Installation

1. Clone the repository:
bash
git clone <repository-url>
cd web-to-md

2. Create and configure your environment file:
```bash
cp .env.example .env
```

Edit `.env` with your API keys and configuration.

3. Build and run with Docker:
```bash
docker compose up -d
```

## Usage

### Command Line

Run the converter using the command line:

```bash
./run.sh
```

Or specify a URL directly:

```bash
./run.sh --url https://example.com
```

### Python Module

```python
from src.convert import MarkdownConverter

converter = MarkdownConverter()
markdown_content = converter.process_url("https://example.com")
```

## Project Structure

The project follows a modular architecture:

```text
web-to-md/
├── src/
│ ├── scrapers/
│ │ ├── html_scraper.py
│ │ └── visual_scraper.py
│ ├── processors/
│ │ ├── content_analyzer.py
│ │ └── layout_analyzer.py
│ ├── converters/
│ │ ├── markdown_converter.py
│ │ └── post_processor.py
│ └── utils/
│ ├── config.py
│ └── validators.py
├── tests/
├── main.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── docs/
```

## Configuration

The application can be configured through environment variables:

- `CHROME_BINARY_PATH`: Path to Chrome/Chromium binary
- `CHROMEDRIVER_PATH`: Path to ChromeDriver
- `ELL_API_KEY`: Your Ell.so API key
- `DEBUG_MODE`: Enable debug logging (true/false)

## Processing Pipeline

1. **Visual Analysis Phase**
   - Screenshot capture
   - Visual importance analysis
   - Content area identification

2. **Content Extraction Phase**
   - Targeted HTML extraction
   - Content cleaning
   - Element correlation

3. **Markdown Conversion Phase**
   - Structured conversion
   - Format preservation
   - Quality validation

## Acknowledgments

- Ell.so for providing the AI-powered content analysis
- Selenium for web automation capabilities
- BeautifulSoup for HTML parsing
- Markdownify for base markdown conversion