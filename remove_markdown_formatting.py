#!/usr/bin/env python3
"""
Script to remove markdown formatting while preserving level 1 (#) and level 2 (##) headings.
Also supports converting cleaned markdown to CSV format with each ## section as a row.
"""

import re
import sys
import argparse
import csv
from pathlib import Path


def remove_markdown_formatting(content):
    """
    Remove all markdown formatting except level 1 (#) and level 2 (##) headings.
    Note: The first level 1 heading will be removed.
    
    Args:
        content (str): The markdown content to process
        
    Returns:
        str: The processed content with formatting removed
    """
    lines = content.split('\n')
    processed_lines = []
    in_code_block = False
    first_h1_encountered = False
    
    for line in lines:
        # Handle code blocks
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue
        
        # Skip content inside code blocks
        if in_code_block:
            # Convert code block content to plain text
            processed_lines.append(line)
            continue
        
        # Check if this is a level 1 heading
        if re.match(r'^#\s+', line):
            if not first_h1_encountered:
                # Skip the first level 1 heading (don't add it to processed_lines)
                first_h1_encountered = True
                continue
            else:
                # Preserve subsequent level 1 headings
                processed_lines.append(line)
                continue
        
        # Preserve level 2 headings
        if re.match(r'^##\s+', line):
            processed_lines.append(line)
            continue
        
        # Convert level 3+ headings to plain text
        line = re.sub(r'^#{3,}\s+', '', line)
        
        # Remove bold formatting (**text** or __text__)
        line = re.sub(r'\*\*(.*?)\*\*', r'\1', line)
        line = re.sub(r'__(.*?)__', r'\1', line)
        
        # Remove italic formatting (*text* or _text_)
        line = re.sub(r'\*(.*?)\*', r'\1', line)
        line = re.sub(r'_(.*?)_', r'\1', line)
        
        # Remove inline code formatting (`text`)
        line = re.sub(r'`([^`]+)`', r'\1', line)
        
        # Remove list formatting (- item, * item, 1. item, etc.)
        line = re.sub(r'^\s*[-*+]\s+', '', line)
        line = re.sub(r'^\s*\d+\.\s+', '', line)
        
        # Remove link formatting [text](url) -> text
        line = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', line)
        
        # Remove reference-style links [text][ref] -> text
        line = re.sub(r'\[([^\]]+)\]\[[^\]]*\]', r'\1', line)
        
        # Remove strikethrough ~~text~~
        line = re.sub(r'~~(.*?)~~', r'\1', line)
        
        # Remove horizontal rules (--- or ***)
        if re.match(r'^[-*]{3,}$', line.strip()):
            continue
        
        # Remove blockquote formatting (> text)
        line = re.sub(r'^\s*>\s*', '', line)
        
        # Remove table formatting (keep content but remove pipes)
        line = re.sub(r'^\s*\|', '', line)
        line = re.sub(r'\|\s*$', '', line)
        line = re.sub(r'\|', ' ', line)
        
        processed_lines.append(line)
    
    return '\n'.join(processed_lines)


def convert_to_csv(content):
    """
    Convert cleaned markdown content to CSV format with each ## section as a row.
    Headings and content are in separate columns.
    
    Args:
        content (str): The cleaned markdown content to process
        
    Returns:
        str: The CSV formatted content
    """
    lines = content.split('\n')
    csv_rows = []
    current_section = []
    current_heading = ""
    
    for line in lines:
        # Check if this is a level 2 heading
        if re.match(r'^##\s+', line):
            # If we have accumulated content, save it as a row
            if current_heading and current_section:
                section_content = '\n'.join(current_section).strip()
                csv_rows.append([current_heading, section_content])
            
            # Start new section - extract only the code portion (before the colon)
            full_heading = re.sub(r'^##\s+', '', line)
            # Extract only the code part (everything before the first colon)
            if ':' in full_heading:
                current_heading = full_heading.split(':')[0].strip()
            else:
                current_heading = full_heading.strip()
            current_section = []
        else:
            # Add content to current section
            current_section.append(line)
    
    # Don't forget the last section
    if current_heading and current_section:
        section_content = '\n'.join(current_section).strip()
        csv_rows.append([current_heading, section_content])
    
    # Create CSV content using proper CSV writer
    from io import StringIO
    output = StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_ALL)
    
    # Write header
    writer.writerow(['Code', 'Content'])
    
    # Write each section as a row
    for heading, content in csv_rows:
        writer.writerow([heading, content])
    
    return output.getvalue()


def main():
    parser = argparse.ArgumentParser(
        description='Remove markdown formatting while preserving level 1 and 2 headings'
    )
    parser.add_argument(
        'input_file',
        help='Input markdown file path'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output file path (default: adds _clean suffix to input filename)'
    )
    parser.add_argument(
        '-c', '--csv',
        action='store_true',
        help='Convert cleaned markdown to CSV format'
    )
    
    args = parser.parse_args()
    
    # Validate input file
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: Input file '{args.input_file}' does not exist", file=sys.stderr)
        sys.exit(1)
    
    if not input_path.suffix.lower() == '.md':
        print(f"Warning: Input file '{args.input_file}' does not have .md extension")
    
    # Determine output file
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = input_path.parent / f"{input_path.stem}_clean{input_path.suffix}"
    
    try:
        # Read input file
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Process content
        cleaned_content = remove_markdown_formatting(content)
        
        if args.csv:
            csv_content = convert_to_csv(cleaned_content)
            output_path = output_path.parent / f"{output_path.stem}.csv"
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(csv_content)
            print(f"Successfully processed '{input_path}' -> '{output_path}'")
        else:
            # Write output file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            
            print(f"Successfully processed '{input_path}' -> '{output_path}'")
            print(f"Original file: {len(content.splitlines())} lines")
            print(f"Cleaned file: {len(cleaned_content.splitlines())} lines")
        
    except Exception as e:
        print(f"Error processing file: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
