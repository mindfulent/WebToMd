# Web to Markdown Converter

## Author: [Jon Pappas](https://github.com/mindfulent)

A powerful Python-based tool that transforms web content into clean, well-formatted Markdown documents by leveraging advanced HTML parsing and GPT-4 Vision-powered analysis. Built with Ell.so for orchestration, it intelligently preserves document structure while eliminating unnecessary elements. 

## Features

- Intelligent content extraction using visual analysis
- HTML parsing with BeautifulSoup
- Visual capture using Selenium
- GPT-4 Vision powered content analysis
- Clean Markdown formatting with customizable rules
- Comprehensive error handling and logging
- Progress tracking for conversion stages

## Example Output

Check out [Markdown.md](output/Markdown.md) for an example of the converter's output when processing the Wikipedia article on Markdown (<https://en.wikipedia.org/wiki/Markdown>). This example demonstrates the tool's ability to:

- Preserve document structure and hierarchy
- Handle complex formatting including tables and code blocks
- Maintain proper link references
- Clean up unnecessary content while keeping essential information
- Format content according to markdown best practices

## Prerequisites

- Python 3.11 or higher
- Chrome/Chromium browser (for Selenium)
- OpenAI via Ell.so framework

## Installation

1. Clone the repository:

```bash
git clone https://github.com/mindfulent/WebToMd
cd WebToMd
```

1. Create and configure your environment file:

```bash
cp .env.example .env
```

Edit `.env` with your API keys and configuration.

1. Set up Python environment and install dependencies:

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

1. Run the converter:

```bash
# Run with URL argument
python -m src.convert --url https://example.com

# Or run interactively
python -m src.convert
```

## Project Structure

The project follows a modular architecture:

```text
web-to-md/
├── src/
│ ├── convert.py
│ └── combine.py
└── README.md
```

## Configuration

The application can be configured through environment variables:

- `OPENAI_API_KEY`: OpenAI API key
- `CHROME_BINARY_PATH`: Path to Chrome/Chromium binary

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