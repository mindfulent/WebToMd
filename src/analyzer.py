import os
import logging
import requests
from bs4 import BeautifulSoup
from typing import Dict, List
from urllib.parse import urlparse
import json
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HTMLAnalyzer:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def analyze_url(self, url: str) -> Dict:
        """Analyze HTML content and structure of a URL"""
        try:
            html_content = self._fetch_content(url)
            
            # Pre-filter JSX content if detected
            if '_jsx' in html_content or 'react' in html_content.lower():
                html_content = self._filter_jsx(html_content)
            
            soup = BeautifulSoup(html_content, 'html.parser')
            
            analysis = {
                'url': url,
                'stats': self._get_content_stats(soup),
                'tag_distribution': self._analyze_tag_distribution(soup),
                'content_quality': self._assess_content_quality(soup),
                'token_estimate': self._estimate_tokens(soup),
                'recommendations': [],
                'processing_strategy': None  # Will be filled below
            }
            
            self._generate_recommendations(analysis)
            analysis['processing_strategy'] = self.determine_processing_strategy(analysis)
            return analysis
            
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            raise

    def _fetch_content(self, url: str) -> str:
        """Fetch HTML content from URL"""
        response = self.session.get(url)
        response.raise_for_status()
        return response.text

    def _filter_jsx(self, html_content: str) -> str:
        """Filter JSX/React specific content"""
        # Using patterns from convert.py filter_jsx_content function
        patterns = [
            r'<script\b[^>]*>[\s\S]*?</script>',
            r'_jsx\([^)]+\)',
            r'_jsxs\([^)]+\)',
            r'className="[^"]*"',
            r'children=\{[^}]*\}',
            r'function \w+\([^)]*\)\s*\{[\s\S]*?\}',
            r'const \{[^}]*\} = [^;]*;'
        ]
        
        for pattern in patterns:
            html_content = re.sub(pattern, '', html_content)
        
        return re.sub(r'\s+', ' ', html_content).strip()

    def _get_content_stats(self, soup: BeautifulSoup) -> Dict:
        """Get basic content statistics"""
        text_content = soup.get_text(strip=True)
        return {
            'total_length': len(str(soup)),
            'text_length': len(text_content),
            'text_ratio': len(text_content) / len(str(soup)) if len(str(soup)) > 0 else 0,
            'tag_count': len(soup.find_all()),
            'script_count': len(soup.find_all('script')),
            'style_count': len(soup.find_all('style')),
            'heading_count': len(soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']))
        }
    
    def _analyze_tag_distribution(self, soup: BeautifulSoup) -> Dict:
        """Analyze distribution of HTML tags"""
        tags = {}
        for tag in soup.find_all():
            tags[tag.name] = tags.get(tag.name, 0) + 1
        return dict(sorted(tags.items(), key=lambda x: x[1], reverse=True))
    
    def _assess_content_quality(self, soup: BeautifulSoup) -> Dict:
        """Assess content quality metrics with API doc focus"""
        # Find the main documentation content area
        main_content = soup.find('main') or soup.find('div', {'class': 'markdown'})
        
        # Look for API-specific elements
        code_blocks = main_content.find_all('pre') if main_content else []
        parameter_sections = main_content.find_all(string=re.compile(r'Parameters|Returns|Examples')) if main_content else []
        method_signature = main_content.find('h1') if main_content else None
        
        return {
            'has_main_content': bool(main_content),
            'is_api_doc': bool(parameter_sections),
            'code_blocks': len(code_blocks),
            'parameter_sections': len(parameter_sections),
            'has_method_signature': bool(method_signature),
            'jsx_detected': any('jsx' in str(tag) or 'react' in str(tag).lower() for tag in soup.find_all()),
            'framework_hints': self._detect_framework(soup)
        }
    
    def _analyze_content_structure(self, soup: BeautifulSoup) -> Dict:
        """Analyze content structure and hierarchy"""
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        heading_levels = [int(h.name[1]) for h in headings]
        
        return {
            'heading_hierarchy': heading_levels,
            'max_heading_depth': max(heading_levels) if heading_levels else 0,
            'min_heading_level': min(heading_levels) if heading_levels else 0,
            'total_sections': len(headings)
        }

    def _estimate_tokens(self, soup: BeautifulSoup) -> Dict:
        """Estimate token count for content processing"""
        text = soup.get_text(strip=True)
        # Rough estimate: 1 token ≈ 4 characters
        estimated_tokens = len(text) // 4
        return {
            'estimated_total_tokens': estimated_tokens,
            'estimated_chunks_needed': (estimated_tokens // 2000) + 1  # GPT-4 context window
        }
    
    def _detect_framework(self, soup: BeautifulSoup) -> str:
        """Detect potential frontend framework"""
        html_str = str(soup)
        frameworks = {
            'React': ['react', '_jsx', 'className='],
            'Vue': ['v-', 'vue'],
            'Angular': ['ng-', 'angular'],
            'Svelte': ['svelte']
        }
        
        for framework, patterns in frameworks.items():
            if any(pattern in html_str.lower() for pattern in patterns):
                return framework
        return 'Unknown'
    
    def _generate_recommendations(self, analysis: Dict):
        """Generate recommendations based on analysis"""
        stats = analysis['stats']
        quality = analysis['content_quality']
        tokens = analysis['token_estimate']
        
        if stats['text_ratio'] < 0.1:
            analysis['recommendations'].append(
                "Low text-to-HTML ratio (high noise). Consider aggressive pre-filtering."
            )
        
        if stats['script_count'] > 10:
            analysis['recommendations'].append(
                "High number of script tags. Enable JSX/script filtering."
            )
            
        if quality['jsx_detected']:
            analysis['recommendations'].append(
                "JSX/React components detected. Enable JSX filtering."
            )
            
        if tokens['estimated_chunks_needed'] > 5:
            analysis['recommendations'].append(
                f"Large content detected ({tokens['estimated_chunks_needed']} chunks). Consider splitting processing."
            )

    def determine_processing_strategy(self, analysis: Dict) -> Dict:
        """Determine optimal processing strategy prioritizing visual analysis"""
        strategy = {
            'preprocessing_steps': [],
            'chunking_method': 'visual_guided',
            'chunk_size': 25000,
            'requires_visual_analysis': True,  # Always use visual analysis first
            'priority_elements': []
        }
        
        # Determine content extraction approach
        if analysis['stats']['text_ratio'] < 0.3:
            strategy['preprocessing_steps'].append('visual_guided_extraction')
            strategy['chunking_method'] = 'visual_sections'
        
        return strategy

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Analyze HTML content of a URL')
    parser.add_argument('url', help='URL to inspect')
    parser.add_argument('--output', '-o', help='Output file for analysis')
    args = parser.parse_args()
    
    analyzer = HTMLAnalyzer()
    analysis = analyzer.analyze_url(args.url)
    
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(analysis, f, indent=2)
    else:
        print(json.dumps(analysis, indent=2))

if __name__ == "__main__":
    main()