import base64
import json
from datetime import datetime
from io import BytesIO, StringIO
from random import randint

import pandas as pd
import streamlit as st


def to_excel(dataframe: pd.DataFrame) -> bytes:
    """
    Converts a DataFrame to Excel format and returns it as bytes.

    Args:
        dataframe (pd.DataFrame): DataFrame to be converted to Excel format.

    Returns:
        bytes: Excel file as bytes.
    """
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        dataframe.to_excel(writer, index=False, sheet_name="Sheet1")
    return output.getvalue()


def get_table_download_link(dataframe: pd.DataFrame, filename: str = "mann_kendall") -> str:
    """
    Generates a button to download a file.

    Args:
        dataframe (pd.DataFrame): DataFrame to be downloaded.
        filename (str, optional): Name of the file to download. Defaults to "mann_kendall".

    Returns:
        str: HTML string representing a button with a href as stream.
    """
    val = to_excel(dataframe)
    b64 = base64.b64encode(val)

    return (
        '<p style="text-align:center;">'
        f'<a href="data:application/octet-stream;base64,{b64.decode()}" '
        f'download="{filename}.xlsx">Download Excel file</a></p>'
    )


def generate_output_filename(original_filename: str = None) -> str:
    """
    Generates a unique filename for the output file.

    Args:
        original_filename (str, optional): Original filename to base the new name on.
            If None, a generic name will be used.

    Returns:
        str: Generated filename with timestamp and random number
    """
    today = datetime.today().strftime("%Y_%m_%d")
    random_number = randint(1000, 5000)

    if original_filename:
        # Extract just the filename without path or extension
        base_name = original_filename.split("/")[-1].split('.')[0]
        return f"{base_name}_{today}_{random_number}"

    return f"mann_kendall_{today}_{random_number}"


def save_to_excel(dataframe: pd.DataFrame, filename: str, output_dir: str = "output_tables") -> str:
    """
    Saves DataFrame to Excel file with a unique filename.

    Args:
        dataframe (pd.DataFrame): DataFrame to save
        filename (str): Base filename
        output_dir (str, optional): Directory to save the file. Defaults to "output_tables".

    Returns:
        str: Full path to the saved file

    Raises:
        FileNotFoundError: If the output directory doesn't exist
        PermissionError: If there are permission issues writing to the file
    """
    # Ensure output directory exists
    import os
    os.makedirs(output_dir, exist_ok=True)

    # Generate unique filename
    output_filename = f"{output_dir}/{generate_output_filename(filename)}.xlsx"

    try:
        # Save DataFrame to Excel
        dataframe.to_excel(output_filename, index=False, sheet_name="mann_kendall")
        return output_filename
    except PermissionError:
        raise PermissionError(f"Cannot write to file {output_filename}. Check permissions.")
    except Exception as e:
        raise OSError(f"Error saving file: {str(e)}")


def create_enhanced_download_section(results: pd.DataFrame, processed_data: pd.DataFrame = None) -> None:
    """
    Create an enhanced download section with multiple export options.

    Args:
        results: Mann-Kendall test results DataFrame
        processed_data: Original processed data DataFrame (optional)
    """
    st.markdown("### 📥 Export Options")

    # Export format selection
    export_format = st.selectbox(
        "Choose Export Format:",
        ["Excel (.xlsx)", "CSV (.csv)", "JSON (.json)", "Summary Report"]
    )

    # Custom filename
    default_name = f"mann_kendall_results_{datetime.now().strftime('%Y%m%d_%H%M')}"
    custom_filename = st.text_input("Filename (without extension):", value=default_name)

    if export_format == "Excel (.xlsx)":
        excel_data = create_excel_export(results, processed_data)
        st.download_button(
            label="📊 Download Excel File",
            data=excel_data,
            file_name=f"{custom_filename}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary"
        )

    elif export_format == "CSV (.csv)":
        csv_data = results.to_csv(index=False)
        st.download_button(
            label="📄 Download CSV File",
            data=csv_data,
            file_name=f"{custom_filename}.csv",
            mime="text/csv",
            type="primary"
        )

    elif export_format == "JSON (.json)":
        json_data = create_json_export(results)
        st.download_button(
            label="🔗 Download JSON File",
            data=json_data,
            file_name=f"{custom_filename}.json",
            mime="application/json",
            type="primary"
        )

    elif export_format == "Summary Report":
        report_data = create_summary_report(results)
        st.download_button(
            label="📋 Download Summary Report",
            data=report_data,
            file_name=f"{custom_filename}_summary.txt",
            mime="text/plain",
            type="primary"
        )

    # Quick export buttons
    st.markdown("**Quick Export:**")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📊 Excel", help="Download as Excel file"):
            excel_data = create_excel_export(results, processed_data)
            st.download_button(
                label="Download Excel",
                data=excel_data,
                file_name=f"{default_name}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    with col2:
        if st.button("📄 CSV", help="Download as CSV file"):
            csv_data = results.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name=f"{default_name}.csv",
                mime="text/csv"
            )

    with col3:
        if st.button("📋 Report", help="Download summary report"):
            report_data = create_summary_report(results)
            st.download_button(
                label="Download Report",
                data=report_data,
                file_name=f"{default_name}_summary.txt",
                mime="text/plain"
            )


def create_excel_export(results: pd.DataFrame, processed_data: pd.DataFrame = None) -> bytes:
    """
    Create an enhanced Excel export with multiple sheets.

    Args:
        results: Mann-Kendall test results
        processed_data: Original processed data (optional)

    Returns:
        Excel file as bytes
    """
    output = BytesIO()

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        # Main results sheet
        results.to_excel(writer, sheet_name="Mann-Kendall Results", index=False)

        # Summary statistics sheet
        summary_stats = create_summary_statistics(results)
        summary_stats.to_excel(writer, sheet_name="Summary Statistics", index=False)

        # Trend summary by well
        well_summary = results.groupby('Well')['Trend'].value_counts().unstack(fill_value=0)
        well_summary.to_excel(writer, sheet_name="Trends by Well")

        # Component summary
        component_summary = results.groupby('Analise')['Trend'].value_counts().unstack(fill_value=0)
        component_summary.to_excel(writer, sheet_name="Trends by Component")

        # Include processed data if available
        if processed_data is not None:
            processed_data.to_excel(writer, sheet_name="Processed Data", index=False)

        # Get workbook and add formatting
        workbook = writer.book

        # Define formats
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#D7E4BC',
            'border': 1
        })

        # Format headers for each sheet
        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            worksheet.set_row(0, None, header_format)
            worksheet.set_column('A:Z', 15)  # Auto-adjust column width

    return output.getvalue()


def create_json_export(results: pd.DataFrame) -> str:
    """
    Create a structured JSON export of the results.

    Args:
        results: Mann-Kendall test results

    Returns:
        JSON string
    """
    export_data = {
        "metadata": {
            "export_date": datetime.now().isoformat(),
            "total_tests": len(results),
            "unique_wells": results['Well'].nunique(),
            "unique_components": results['Analise'].nunique()
        },
        "summary": {
            "trend_distribution": results['Trend'].value_counts().to_dict(),
            "wells_with_trends": len(results[results['Trend'] != 'no trend']['Well'].unique()),
            "components_analyzed": results['Analise'].unique().tolist()
        },
        "results": results.to_dict('records')
    }

    return json.dumps(export_data, indent=2, default=str)


def create_summary_report(results: pd.DataFrame) -> str:
    """
    Create a text-based summary report.

    Args:
        results: Mann-Kendall test results

    Returns:
        Summary report as string
    """
    report = StringIO()

    # Header
    report.write("MANN-KENDALL TREND ANALYSIS SUMMARY REPORT\n")
    report.write("=" * 50 + "\n\n")

    # Generation info
    report.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report.write(f"Total Tests Performed: {len(results)}\n")
    report.write(f"Unique Wells: {results['Well'].nunique()}\n")
    report.write(f"Components Analyzed: {results['Analise'].nunique()}\n\n")

    # Trend summary
    report.write("TREND DISTRIBUTION\n")
    report.write("-" * 20 + "\n")
    trend_counts = results['Trend'].value_counts()
    for trend, count in trend_counts.items():
        percentage = (count / len(results)) * 100
        report.write(f"{trend.title()}: {count} ({percentage:.1f}%)\n")

    report.write("\n")

    # Wells with significant trends
    significant_wells = results[results['Trend'] != 'no trend']['Well'].unique()
    report.write(f"WELLS WITH SIGNIFICANT TRENDS ({len(significant_wells)} wells)\n")
    report.write("-" * 40 + "\n")

    for well in sorted(significant_wells):
        well_trends = results[
            (results['Well'] == well) & (results['Trend'] != 'no trend')
        ]
        report.write(f"\n{well}:\n")
        for _, row in well_trends.iterrows():
            report.write(f"  - {row['Analise']}: {row['Trend']} (S={row['Mann-Kendall Statistic (S)']:.2f})\n")

    # Component analysis
    report.write("\n\nCOMPONENT ANALYSIS\n")
    report.write("-" * 20 + "\n")

    for component in sorted(results['Analise'].unique()):
        component_data = results[results['Analise'] == component]
        trend_dist = component_data['Trend'].value_counts()
        report.write(f"\n{component}:\n")
        for trend, count in trend_dist.items():
            report.write(f"  - {trend}: {count}\n")

    return report.getvalue()


def create_summary_statistics(results: pd.DataFrame) -> pd.DataFrame:
    """
    Create summary statistics DataFrame for Excel export.

    Args:
        results: Mann-Kendall test results

    Returns:
        Summary statistics DataFrame
    """
    summary_data = []

    # Overall statistics
    summary_data.append({
        'Metric': 'Total Tests',
        'Value': len(results),
        'Description': 'Total number of Mann-Kendall tests performed'
    })

    summary_data.append({
        'Metric': 'Unique Wells',
        'Value': results['Well'].nunique(),
        'Description': 'Number of unique monitoring wells/points'
    })

    summary_data.append({
        'Metric': 'Components Analyzed',
        'Value': results['Analise'].nunique(),
        'Description': 'Number of different components/parameters tested'
    })

    # Trend statistics
    trend_counts = results['Trend'].value_counts()
    for trend, count in trend_counts.items():
        percentage = (count / len(results)) * 100
        summary_data.append({
            'Metric': f'{trend.title()} Trends',
            'Value': f'{count} ({percentage:.1f}%)',
            'Description': f'Tests showing {trend} trend'
        })

    # Statistical ranges
    summary_data.append({
        'Metric': 'Mann-Kendall Statistic Range',
        'Value': f'{results["Mann-Kendall Statistic (S)"].min():.2f} to {results["Mann-Kendall Statistic (S)"].max():.2f}',
        'Description': 'Range of Mann-Kendall S statistics'
    })

    summary_data.append({
        'Metric': 'Confidence Factor Range',
        'Value': f'{results["Confidence Factor"].min():.2f} to {results["Confidence Factor"].max():.2f}',
        'Description': 'Range of confidence factors'
    })

    return pd.DataFrame(summary_data)