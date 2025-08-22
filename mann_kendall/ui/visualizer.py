from typing import List

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


def filter_well_component(
    df_transposed: pd.DataFrame, desired_wells: list, desired_component: str
) -> pd.DataFrame:
    """
    Filters the DataFrame to include only the desired wells and component.

    Args:
        df_transposed (pd.DataFrame): Transposed DataFrame.
        desired_wells (list): List of desired wells.
        desired_component (str): Desired component selected by the user.

    Returns:
        pd.DataFrame: Filtered DataFrame.
    """
    df_filtered = df_transposed[df_transposed.well.isin(desired_wells)]
    df_filtered = df_filtered[["well", "Date", desired_component]].sort_values("Date")
    df_filtered[desired_component] = df_filtered[desired_component].apply(float)
    df_filtered = df_filtered.reset_index(drop=True)
    return df_filtered


def get_desired_component(results: pd.DataFrame, desired_wells: List[str]) -> str:
    """
    Gets the desired component selected by the user.

    Args:
        results (pd.DataFrame): Results of the Mann Kendall test.
        desired_wells (list): List of desired wells.

    Returns:
        str: Desired component selected by the user.
    """
    results_filter_by_well = results[results.Well.isin(desired_wells)]
    desired_component = st.selectbox(
        "Select Component", results_filter_by_well.Analise.unique()
    )
    return desired_component


def choose_log_scale() -> bool:
    """
    Allows the user to choose between a logarithmic or linear scale for the y-axis.

    Returns:
        bool: True if log scale is selected, False otherwise.
    """
    log_scale = st.selectbox("Select Scale", ["Log", "Linear"])
    return log_scale == "Log"


def create_trend_plot(results: pd.DataFrame, dataframe: pd.DataFrame) -> None:
    """
    Creates and displays an interactive plot of selected wells and components.

    Args:
        results (pd.DataFrame): Results of the Mann Kendall test.
        dataframe (pd.DataFrame): DataFrame containing the data.
    """
    st.subheader("📈 Interactive Trend Visualization")

    # Enhanced well selection with search and filtering
    col1, col2 = st.columns([2, 1])

    with col1:
        # Add quick selection options
        all_wells = results.Well.unique()

        selection_type = st.radio(
            "Selection Method:",
            ["Manual Selection", "Wells with Trends", "All Wells"],
            horizontal=True
        )

        if selection_type == "Manual Selection":
            desired_wells = st.multiselect(
                "Select Wells to Plot",
                all_wells,
                help="Choose specific wells to visualize"
            )
        elif selection_type == "Wells with Trends":
            trending_wells = results[results.Trend != 'no trend'].Well.unique()
            desired_wells = st.multiselect(
                "Wells with Significant Trends",
                trending_wells,
                default=trending_wells[:5] if len(trending_wells) > 0 else [],
                help="Pre-filtered to wells with detected trends"
            )
        else:  # All Wells
            desired_wells = st.multiselect(
                "All Wells",
                all_wells,
                default=all_wells[:3] if len(all_wells) > 0 else [],
                help="All available wells (limited to first 3 by default for performance)"
            )

    with col2:
        if len(desired_wells) > 0:
            # Show trend information for selected wells
            st.write("**Trend Summary:**")
            selected_results = results[results.Well.isin(desired_wells)]
            trend_summary = selected_results.Trend.value_counts()

            for trend, count in trend_summary.items():
                if 'increasing' in trend:
                    st.success(f"📈 {count} {trend}")
                elif 'decreasing' in trend:
                    st.error(f"📉 {count} {trend}")
                else:
                    st.info(f"➡️ {count} {trend}")

    if len(desired_wells) > 0:
        # Component selection with better UX
        desired_component = get_desired_component(results, desired_wells)

        # Visualization options
        col1, col2, col3 = st.columns(3)

        with col1:
            log_scale = choose_log_scale()

        with col2:
            show_points = st.checkbox("Show Data Points", value=True)

        with col3:
            smooth_lines = st.checkbox("Smooth Lines", value=False)

        # Filter and prepare data
        df_filtered = filter_well_component(dataframe, desired_wells, desired_component)
        df_filtered = df_filtered.dropna()

        if df_filtered.empty:
            st.warning("⚠️ No data available for the selected wells and component combination.")
            return

        # Prepare data for plotting
        df_plot = df_filtered.reset_index(drop=True).ffill()

        # Handle log scale properly
        if log_scale:
            min_value = df_plot[desired_component].min()
            log_component_name = f"{desired_component}_log"

            if min_value <= 0:
                st.warning(
                    f"⚠️ **Log Scale Notice:** Data contains zeros or negative values (min: {min_value:.3f}). "
                    f"These will be replaced with small positive values for visualization."
                )

                positive_min = df_plot[df_plot[desired_component] > 0][desired_component].min()
                replacement_value = positive_min * 0.01 if not pd.isna(positive_min) else 0.001

                df_plot[log_component_name] = df_plot[desired_component].copy()
                df_plot.loc[df_plot[log_component_name] <= 0, log_component_name] = replacement_value
                df_plot[log_component_name] = np.log10(df_plot[log_component_name])

                title = f"{desired_component} Trends (Log Scale - Adjusted Values)"
                plot_component = log_component_name
                y_title = f"Log₁₀({desired_component})"
            else:
                df_plot[log_component_name] = np.log10(df_plot[desired_component])
                title = f"{desired_component} Trends (Log Scale)"
                plot_component = log_component_name
                y_title = f"Log₁₀({desired_component})"
        else:
            title = f"{desired_component} Trends (Linear Scale)"
            plot_component = desired_component
            y_title = desired_component

        # Create the plot with enhanced styling
        if smooth_lines:
            fig = px.line(
                df_plot,
                x="Date",
                y=plot_component,
                color="well",
                title=title,
                line_shape="spline"
            )
        else:
            fig = px.line(
                df_plot,
                x="Date",
                y=plot_component,
                color="well",
                title=title
            )

        # Add scatter points if requested
        if show_points:
            fig.update_traces(mode='lines+markers', marker=dict(size=4))

        # Enhanced styling
        fig.update_layout(
            yaxis_title=y_title,
            xaxis_title="Date",
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            height=500
        )

        # Add trend annotations for each well
        for well in desired_wells:
            well_trend_data = results[
                (results.Well == well) & (results.Analise == desired_component)
            ]
            if not well_trend_data.empty:
                trend = well_trend_data.iloc[0]['Trend']
                if trend != 'no trend':
                    # Add subtle trend indicator
                    if 'increasing' in trend:
                        trend_symbol = "📈"
                    elif 'decreasing' in trend:
                        trend_symbol = "📉"
                    else:
                        trend_symbol = "➡️"

                    fig.add_annotation(
                        text=f"{well}: {trend_symbol}",
                        xref="paper", yref="paper",
                        x=0.02, y=0.98 - (list(desired_wells).index(well) * 0.05),
                        showarrow=False,
                        font=dict(size=10),
                        bgcolor="rgba(255,255,255,0.8)",
                        bordercolor="gray",
                        borderwidth=1
                    )

        st.plotly_chart(fig, use_container_width=True)

        # Show data statistics
        with st.expander("📊 Data Statistics for Selected Wells"):
            stats_df = df_filtered.groupby('well')[desired_component].agg([
                'count', 'mean', 'std', 'min', 'max'
            ]).round(3)
            stats_df.columns = ['Data Points', 'Mean', 'Std Dev', 'Min', 'Max']
            st.dataframe(stats_df, use_container_width=True)

    else:
        st.info("👆 Please select one or more wells to create visualizations.")


def display_results_table(results: pd.DataFrame) -> None:
    """
    Displays the results table with enhanced filtering and sorting options.

    Args:
        results (pd.DataFrame): Results of the Mann Kendall test.
    """
    st.subheader("📋 Detailed Results Table")

    # Enhanced filtering options
    col1, col2, col3 = st.columns(3)

    with col1:
        well_filter = st.multiselect(
            "🏭 Filter by Wells",
            options=sorted(results.Well.unique()),
            default=[],
            help="Select specific wells to view"
        )

    with col2:
        trend_filter = st.multiselect(
            "📈 Filter by Trend",
            options=results.Trend.unique(),
            default=[],
            help="Filter by trend type"
        )

    with col3:
        component_filter = st.multiselect(
            "🧪 Filter by Component",
            options=sorted(results.Analise.unique()),
            default=[],
            help="Select specific components"
        )

    # Additional filtering options
    col1, col2 = st.columns(2)

    with col1:
        # Confidence factor threshold
        min_conf = float(results['Confidence Factor'].min())
        max_conf = float(results['Confidence Factor'].max())

        # Only show slider if there's a range of values
        if max_conf > min_conf:
            min_confidence = st.slider(
                "Minimum Confidence Factor",
                min_value=min_conf,
                max_value=max_conf,
                value=min_conf,
                step=0.1,
                help="Filter results by minimum confidence level"
            )
        else:
            # If all values are the same, just show the value and use it as filter
            st.write(f"**Confidence Factor:** {min_conf:.2f} (all results)")
            min_confidence = min_conf

    with col2:
        # Show only significant trends option
        only_significant = st.checkbox(
            "Show Only Significant Trends",
            help="Hide results with 'no trend'"
        )

    # Apply filters
    filtered_results = results.copy()

    if well_filter:
        filtered_results = filtered_results[filtered_results.Well.isin(well_filter)]
    if trend_filter:
        filtered_results = filtered_results[filtered_results.Trend.isin(trend_filter)]
    if component_filter:
        filtered_results = filtered_results[filtered_results.Analise.isin(component_filter)]
    if only_significant:
        filtered_results = filtered_results[filtered_results.Trend != 'no trend']

    filtered_results = filtered_results[
        filtered_results['Confidence Factor'] >= min_confidence
    ]

    # Display summary of filtered results
    if len(filtered_results) != len(results):
        st.info(f"📊 Showing {len(filtered_results)} of {len(results)} results after filtering")

    # Sorting options
    col1, col2 = st.columns(2)

    with col1:
        sort_column = st.selectbox(
            "Sort by:",
            options=['Well', 'Analise', 'Trend', 'Mann-Kendall Statistic (S)', 'Confidence Factor'],
            index=0
        )

    with col2:
        sort_ascending = st.selectbox("Sort order:", ["Ascending", "Descending"]) == "Ascending"

    # Apply sorting
    if not filtered_results.empty:
        filtered_results = filtered_results.sort_values(
            by=sort_column,
            ascending=sort_ascending
        ).reset_index(drop=True)

        # Style the dataframe for better readability
        def style_trends(val):
            if 'increasing' in val:
                return 'background-color: #d4edda; color: #155724'
            elif 'decreasing' in val:
                return 'background-color: #f8d7da; color: #721c24'
            else:
                return 'background-color: #d1ecf1; color: #0c5460'

        # Display the styled results
        styled_df = filtered_results.style.map(
            style_trends,
            subset=['Trend']
        ).format({
            'Mann-Kendall Statistic (S)': '{:.2f}',
            'Coefficient of Variation': '{:.4f}',
            'Confidence Factor': '{:.2f}'
        })

        st.dataframe(styled_df, use_container_width=True, height=400)

        # Export options for filtered data
        if st.button("📥 Download Filtered Results", type="secondary"):
            csv = filtered_results.to_csv(index=False)
            st.download_button(
                label="Download as CSV",
                data=csv,
                file_name="mann_kendall_filtered_results.csv",
                mime="text/csv"
            )

    else:
        st.warning("⚠️ No results match the current filter criteria. Try adjusting your filters.")

    # Quick statistics for filtered results
    if not filtered_results.empty:
        with st.expander("📊 Quick Statistics for Filtered Results"):
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Total Results", len(filtered_results))
            with col2:
                st.metric("Unique Wells", filtered_results.Well.nunique())
            with col3:
                st.metric("Unique Components", filtered_results.Analise.nunique())
            with col4:
                significant_count = len(filtered_results[filtered_results.Trend != 'no trend'])
                st.metric("Significant Trends", significant_count)

            # Trend distribution for filtered results
            trend_dist = filtered_results.Trend.value_counts()
            st.write("**Trend Distribution:**")
            for trend, count in trend_dist.items():
                percentage = (count / len(filtered_results)) * 100
                st.write(f"- {trend.title()}: {count} ({percentage:.1f}%)")