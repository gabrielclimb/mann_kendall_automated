#!/usr/bin/env python

"""
Command line interface for Mann Kendall Automated.

Allows processing Excel files via command line and saving results.
Supports batch processing, verbose output, and various export formats.
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

# Add the parent directory to Python path so we can import the package
sys.path.insert(0, str(Path(__file__).parent.parent))

from mann_kendall.core.processor import generate_mann_kendall
from mann_kendall.data.loader import load_excel_data
from mann_kendall.utils.logging_config import setup_logging


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Mann Kendall Automated - Trend Analysis CLI",
        epilog="Examples:\n"
        "  %(prog)s data.xlsx\n"
        "  %(prog)s data.xlsx -o results.xlsx --verbose\n"
        "  %(prog)s data.xlsx --format csv --log-level DEBUG\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "input_file",
        help="Path to input Excel file (.xlsx or .xls)",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Path to output file (default: <input>_mann_kendall_results.<format>)",
    )
    parser.add_argument(
        "--format",
        choices=["xlsx", "csv", "json"],
        default="xlsx",
        help="Output format (default: xlsx)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print detailed progress information",
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level (default: INFO)",
    )
    parser.add_argument(
        "--log-file",
        help="Path to log file (optional, logs to console if not specified)",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print summary statistics after processing",
    )

    return parser.parse_args()


def print_summary(results):
    """
    Print summary statistics of the analysis results.

    Args:
        results: DataFrame with Mann-Kendall test results
    """
    print("\n" + "=" * 60)
    print("MANN-KENDALL ANALYSIS SUMMARY")
    print("=" * 60)

    total_analyses = len(results)
    unique_wells = len(results["Well"].unique())
    unique_components = len(results["Analise"].unique())

    print(f"Total analyses performed: {total_analyses}")
    print(f"Unique wells: {unique_wells}")
    print(f"Unique components: {unique_components}")

    print("\nTrend Distribution:")
    trend_counts = results["Trend"].value_counts()
    for trend, count in trend_counts.items():
        percentage = (count / total_analyses) * 100
        print(f"  {trend:25s}: {count:4d} ({percentage:5.1f}%)")

    if "Confidence Factor" in results.columns:
        avg_cf = results["Confidence Factor"].mean()
        print(f"\nAverage Confidence Factor: {avg_cf:.3f}")

    print("=" * 60 + "\n")


def main():
    """Main CLI function."""
    args = parse_args()

    # Setup logging
    logger = setup_logging(
        level=args.log_level,
        log_file=args.log_file,
    )

    start_time = datetime.now()

    # Validate input file
    if not os.path.exists(args.input_file):
        logger.error("Input file not found: %s", args.input_file)
        sys.exit(f"Error: Input file '{args.input_file}' not found.")

    logger.info("Starting Mann-Kendall analysis")
    logger.info("Input file: %s", args.input_file)

    if args.verbose:
        print(f"Processing file: {args.input_file}")
        print(f"Log level: {args.log_level}")
        print(f"Output format: {args.format}")

    try:
        # Load data
        logger.info("Loading data from Excel file...")
        df = load_excel_data(args.input_file)
        logger.info("Data loaded successfully: %d rows, %d columns", len(df), len(df.columns))

        if args.verbose:
            print(f"Loaded {len(df)} rows with {len(df.columns)} wells")

        # Process data
        logger.info("Running Mann-Kendall analysis...")
        results, df_transposed = generate_mann_kendall(df)
        logger.info("Analysis complete: %d results generated", len(results))

        # Determine output file path
        output_file = args.output
        if not output_file:
            base_name = os.path.splitext(os.path.basename(args.input_file))[0]
            output_file = f"{base_name}_mann_kendall_results.{args.format}"

        # Save results based on format
        logger.info("Saving results to: %s", output_file)
        if args.format == "xlsx":
            results.to_excel(output_file, index=False)
        elif args.format == "csv":
            results.to_csv(output_file, index=False)
        elif args.format == "json":
            results.to_json(output_file, orient="records", indent=2)

        elapsed_time = (datetime.now() - start_time).total_seconds()
        logger.info("Processing completed in %.2f seconds", elapsed_time)

        if args.verbose:
            print(f"\n✓ Results saved to: {output_file}")
            print(f"✓ Processed {len(results)} component analyses")
            print(f"✓ Wells analyzed: {len(results['Well'].unique())}")
            print(f"✓ Time elapsed: {elapsed_time:.2f} seconds")
        else:
            print(output_file)

        # Print summary if requested
        if args.summary or args.verbose:
            print_summary(results)

    except FileNotFoundError as e:
        logger.error("File not found: %s", e)
        sys.exit(f"Error: {e}")
    except ValueError as e:
        logger.error("Invalid data: %s", e)
        sys.exit(f"Error: {e}")
    except Exception as e:
        logger.exception("Unexpected error occurred")
        sys.exit(f"Error processing file: {e}")


if __name__ == "__main__":
    main()