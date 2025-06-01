"""Tests for visualizer.py module."""

from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from mann_kendall.ui.visualizer import (
    choose_log_scale,
    create_trend_plot,
    filter_well_component,
    get_desired_component,
    display_results_table,
)


def test_filter_well_component():
    """Test filter_well_component function."""
    # Create a sample DataFrame
    df = pd.DataFrame({
        "well": ["Well1", "Well2", "Well3"],
        "Date": ["2020-01-01", "2020-01-02", "2020-01-03"],
        "Component1": ["5.0", "6.0", "7.0"],
    })
    
    # Filter the DataFrame
    filtered_df = filter_well_component(df, ["Well1", "Well2"], "Component1")
    
    # Check the filtered DataFrame
    assert len(filtered_df) == 2
    assert "Well3" not in filtered_df["well"].values
    assert filtered_df["Component1"].dtype == float
    assert filtered_df["Component1"].tolist() == [5.0, 6.0]


def test_get_desired_component():
    results = pd.DataFrame({'Well': ['A', 'B'], 'Analise': ['X', 'Y']})
    with patch('streamlit.selectbox', return_value='X'):
        component = get_desired_component(results, ['A', 'B'])
        assert component == 'X'


@patch("streamlit.selectbox")
def test_choose_log_scale_log(mock_selectbox):
    """Test choose_log_scale returns True for Log scale."""
    mock_selectbox.return_value = "Log"
    assert choose_log_scale() is True
    mock_selectbox.assert_called_once_with("Select Scale", ["Log", "Linear"])


@patch("streamlit.selectbox")
def test_choose_log_scale_linear(mock_selectbox):
    """Test choose_log_scale returns False for Linear scale."""
    mock_selectbox.return_value = "Linear"
    assert choose_log_scale() is False
    mock_selectbox.assert_called_once_with("Select Scale", ["Log", "Linear"])


@patch("streamlit.multiselect")
@patch("mann_kendall.ui.visualizer.get_desired_component")
@patch("mann_kendall.ui.visualizer.filter_well_component")
@patch("mann_kendall.ui.visualizer.choose_log_scale")
@patch("plotly.express.line")
@patch("streamlit.plotly_chart")
@patch("streamlit.warning")
def test_create_trend_plot_log_scale(
    mock_warning, mock_plotly_chart, mock_line, mock_choose_log_scale, 
    mock_filter, mock_get_component, mock_multiselect):
    """Test create_trend_plot with log scale."""
    # Mock data
    results = pd.DataFrame({"Well": ["Well1", "Well2"], "Analise": ["Component1", "Component1"]})
    dataframe = pd.DataFrame({
        "well": ["Well1", "Well2"],
        "Date": ["2020-01-01", "2020-01-02"],
        "Component1": [5.0, 6.0],
    })
    
    # Configure mocks
    mock_multiselect.return_value = ["Well1"]
    mock_get_component.return_value = "Component1"
    mock_filter.return_value = dataframe
    mock_choose_log_scale.return_value = True  # Log scale
    mock_figure = MagicMock()
    mock_line.return_value = mock_figure
    
    # Call function
    create_trend_plot(results, dataframe)
    
    # Check log_y parameter is False (we manually transform)
    _, kwargs = mock_line.call_args
    assert kwargs["log_y"] is False
    
    # No warnings should be shown since all values are positive
    mock_warning.assert_not_called()
    
    # Verify title contains log scale
    assert "log scale" in kwargs["title"]
    
    # Verify we're plotting the log-transformed column
    assert kwargs["y"] == "Component1_log"
    
    # Verify y-axis title is still the original component
    mock_line.return_value.update_layout.assert_called_once_with(yaxis_title="Component1")


@patch("streamlit.multiselect")
@patch("mann_kendall.ui.visualizer.get_desired_component")
@patch("mann_kendall.ui.visualizer.filter_well_component")
@patch("mann_kendall.ui.visualizer.choose_log_scale")
@patch("plotly.express.line")
@patch("streamlit.plotly_chart")
@patch("streamlit.warning")
def test_create_trend_plot_log_scale_with_zeros(mock_warning, mock_plotly_chart, mock_line, 
                                               mock_choose_log_scale, mock_filter, 
                                               mock_get_component, mock_multiselect):
    """Test create_trend_plot with log scale and zeros in data."""
    # Mock data
    results = pd.DataFrame({"Well": ["Well1", "Well2"], "Analise": ["Component1", "Component1"]})
    dataframe = pd.DataFrame({
        "well": ["Well1", "Well2"],
        "Date": ["2020-01-01", "2020-01-02"],
        "Component1": [0.0, 6.0],  # First value is zero
    })
    
    # Configure mocks
    mock_multiselect.return_value = ["Well1"]
    mock_get_component.return_value = "Component1"
    mock_filter.return_value = dataframe
    mock_choose_log_scale.return_value = True  # Log scale
    mock_figure = MagicMock()
    mock_line.return_value = mock_figure
    
    # Call function
    create_trend_plot(results, dataframe)
    
    # Check that warning was shown for zero values
    mock_warning.assert_called_once()
    
    # Verify we're plotting the log-transformed column
    _, kwargs = mock_line.call_args
    assert kwargs["y"] == "Component1_log"
    
    # Verify title mentions replaced values
    assert "replaced values" in kwargs["title"]
    
    # Verify log_y is False since we manually transform
    assert kwargs["log_y"] is False


@patch("streamlit.multiselect")
@patch("mann_kendall.ui.visualizer.get_desired_component")
@patch("mann_kendall.ui.visualizer.filter_well_component")
@patch("mann_kendall.ui.visualizer.choose_log_scale")
@patch("plotly.express.line")
@patch("streamlit.plotly_chart")
@patch("streamlit.warning")
def test_create_trend_plot_linear_scale(
    mock_warning, mock_plotly_chart, mock_line, mock_choose_log_scale,
    mock_filter, mock_get_component, mock_multiselect):
    """Test create_trend_plot with linear scale."""
    # Mock data
    results = pd.DataFrame({"Well": ["Well1", "Well2"], "Analise": ["Component1", "Component1"]})
    dataframe = pd.DataFrame({
        "well": ["Well1", "Well2"],
        "Date": ["2020-01-01", "2020-01-02"],
        "Component1": [5.0, 6.0],
    })
    
    # Configure mocks
    mock_multiselect.return_value = ["Well1"]
    mock_get_component.return_value = "Component1"
    mock_filter.return_value = dataframe
    mock_choose_log_scale.return_value = False  # Linear scale
    mock_figure = MagicMock()
    mock_line.return_value = mock_figure
    
    # Call function
    create_trend_plot(results, dataframe)
    
    # Check we're using the original component
    _, kwargs = mock_line.call_args
    assert kwargs["y"] == "Component1"
    
    # Verify log_y is False
    assert kwargs["log_y"] is False
    
    # No warnings should be shown
    mock_warning.assert_not_called()
    
    # Verify title contains linear scale
    assert "linear scale" in kwargs["title"]


def test_create_trend_plot():
    results = pd.DataFrame({'Well': ['A', 'B'], 'Analise': ['X', 'Y']})
    dataframe = pd.DataFrame({'well': ['A', 'B'], 'Date': ['2020-01-01', '2020-01-02'], 'X': [1, 2]})
    with patch('streamlit.multiselect', return_value=['A', 'B']):
        with patch('streamlit.selectbox', return_value='X'):
            with patch('streamlit.plotly_chart'):
                create_trend_plot(results, dataframe)


def test_display_results_table():
    results = pd.DataFrame({'Well': ['A', 'B'], 'Trend': ['Up', 'Down']})
    with patch('streamlit.multiselect', return_value=['A']):
        with patch('streamlit.dataframe'):
            display_results_table(results)