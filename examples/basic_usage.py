
"""
Basic usage example for Mann Kendall Automated package.
"""

import matplotlib.pyplot as plt

from mann_kendall.core.processor import generate_mann_kendall
from mann_kendall.data.loader import load_excel_data


def main():
    """Example of using the Mann Kendall package programmatically."""
    # Load data
    print("Loading data...")
    df = load_excel_data("example_input_table.xlsx")
    
    # Run Mann-Kendall analysis
    print("Running Mann-Kendall analysis...")
    results, transposed_data = generate_mann_kendall(df)
    
    # Display results
    print("\nMann-Kendall Results:")
    print(f"Processed {len(results)} components from {len(results.Well.unique())} wells")
    
    # Show summary by trend
    trend_summary = results.Trend.value_counts()
    print("\nTrend Summary:")
    print(trend_summary)
    
    # Save results
    results.to_excel("example_results.xlsx", index=False)
    print("\nResults saved to 'example_results.xlsx'")
    
    # Create a simple visualization
    plt.figure(figsize=(10, 6))
    trend_summary.plot(kind='bar', color='skyblue')
    plt.title('Mann-Kendall Trend Analysis Results')
    plt.xlabel('Trend Type')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig('trend_summary.png')
    print("Visualization saved to 'trend_summary.png'")


if __name__ == "__main__":
    main()