#!/bin/bash
# Example of using the Mann Kendall CLI tool

# Process a single file
echo "Processing a single file..."
mann-kendall example_input_table.xlsx -o single_result.xlsx

# Process multiple files with a loop
echo "Processing multiple files..."
for file in ../*_input_table*.xlsx; do
  filename=$(basename "$file")
  echo "Processing $filename..."
  mann-kendall "$file" -o "${filename%.*}_results.xlsx" --verbose
done

echo "Done! All files processed."