#!/usr/bin/env python

"""
Command line interface for Mann Kendall Automated.
Allows processing Excel files via command line and saving results.
"""

import argparse
import os
import sys
from pathlib import Path

# Add the parent directory to Python path so we can import the package
sys.path.insert(0, str(Path(__file__).parent.parent))

from mann_kendall.core.processor import generate_mann_kendall
from mann_kendall.data.loader import load_excel_data


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Mann Kendall Automated - Command Line Interface"
    )
    parser.add_argument(
        "input_file", 
        help="Path to input Excel file (.xlsx or .xls)"
    )
    parser.add_argument(
        "-o", "--output", 
        help="Path to output Excel file (default: mann_kendall_result.xlsx)"
    )
    parser.add_argument(
        "--verbose", 
        action="store_true", 
        help="Print verbose output"
    )
    
    return parser.parse_args()


def main():
    """Main CLI function."""
    args = parse_args()
    
    # Validate input file
    if not os.path.exists(args.input_file):
        sys.exit(f"Error: Input file '{args.input_file}' not found.")
    
    if args.verbose:
        print(f"Processing file: {args.input_file}")
    
    try:
        # Load data
        df = load_excel_data(args.input_file)
        
        # Process data
        results, _ = generate_mann_kendall(df)
        
        # Determine output file path
        output_file = args.output
        if not output_file:
            base_name = os.path.splitext(os.path.basename(args.input_file))[0]
            output_file = f"{base_name}_mann_kendall_results.xlsx"
        
        # Save results
        results.to_excel(output_file, index=False)
        
        if args.verbose:
            print(f"Results saved to: {output_file}")
            print(f"Processed {len(results)} components from {len(results.Well.unique())} wells")
        else:
            print(output_file)
            
    except Exception as e:
        sys.exit(f"Error processing file: {e}")


if __name__ == "__main__":
    main()