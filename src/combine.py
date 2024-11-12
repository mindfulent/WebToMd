"""
Markdown File Combiner
A tool that combines multiple markdown files with a given prefix into a single markdown file.
"""

import os
import argparse
import logging
from typing import List, Optional
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

class MarkdownCombiner:
    """Combines multiple markdown files into a single document"""
    
    def __init__(self, input_dir: str = "output"):
        self.input_dir = input_dir
        
    def find_markdown_files(self, prefix: str) -> List[str]:
        """Find all markdown files with given prefix"""
        files = []
        try:
            for filename in os.listdir(self.input_dir):
                if filename.startswith(prefix) and filename.endswith('.md'):
                    files.append(os.path.join(self.input_dir, filename))
            return sorted(files)  # Sort files to ensure consistent order
        except Exception as e:
            logger.error(f"Error finding markdown files: {e}")
            raise

    def combine_files(self, files: List[str], output_file: str) -> None:
        """Combine multiple markdown files into one"""
        try:
            with open(output_file, 'w', encoding='utf-8') as outfile:
                for i, file in enumerate(files):
                    logger.info(f"Processing file {i+1}/{len(files)}: {file}")
                    
                    with open(file, 'r', encoding='utf-8') as infile:
                        content = infile.read().strip()
                        
                        # Add separator between files if not the first file
                        if i > 0:
                            outfile.write('\n\n---\n\n')
                        
                        outfile.write(content)
                        outfile.write('\n')  # Ensure newline at end of file
                        
            logger.info(f"Successfully combined {len(files)} files into {output_file}")
            
        except Exception as e:
            logger.error(f"Error combining files: {e}")
            raise

    def process(self, prefix: str, output_file: Optional[str] = None) -> str:
        """Process files with given prefix and combine them"""
        try:
            # Find all matching files
            files = self.find_markdown_files(prefix)
            
            if not files:
                logger.error(f"No markdown files found with prefix '{prefix}'")
                raise FileNotFoundError(f"No files found with prefix '{prefix}'")
            
            # Generate output filename if not provided
            if not output_file:
                output_file = os.path.join(self.input_dir, f"{prefix}_combined.md")
            
            # Combine the files
            self.combine_files(files, output_file)
            return output_file
            
        except Exception as e:
            logger.error(f"Error processing files: {e}")
            raise

def main():
    """Main function to run the combiner"""
    parser = argparse.ArgumentParser(description='Combine markdown files with a given prefix')
    parser.add_argument('--prefix', help='Prefix of files to combine')
    parser.add_argument('--output', help='Output file path (optional)')
    parser.add_argument('--input-dir', help='Input directory (default: output)', default='output')
    args = parser.parse_args()
    
    prefix = args.prefix
    if not prefix:
        prefix = input("Please enter the prefix of files to combine: ").strip()
    
    if not prefix:
        logger.error("No prefix provided")
        return
    
    combiner = MarkdownCombiner(input_dir=args.input_dir)
    try:
        output_file = combiner.process(prefix, args.output)
        logger.info(f"Files successfully combined into: {output_file}")
    except Exception as e:
        logger.error(f"Combination failed: {e}")
        raise

if __name__ == "__main__":
    main()
