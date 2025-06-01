import pytest
from mann_kendall.utils.progress import print_progress_bar
from io import StringIO
import sys

def test_print_progress_bar():
    # Redirect stdout to capture printed output
    captured_output = StringIO()
    sys.stdout = captured_output

    # Test basic progress bar
    print_progress_bar(50, 100, prefix="Progress:", suffix="Complete", length=50)
    output = captured_output.getvalue()
    assert "Progress:" in output
    assert "50.0%" in output
    assert "Complete" in output

    # Test progress bar with custom fill
    print_progress_bar(75, 100, fill="*", length=50)
    output = captured_output.getvalue()
    assert "*" in output

    # Test progress bar with different decimals
    print_progress_bar(33, 100, decimals=2)
    output = captured_output.getvalue()
    assert "33.00%" in output

    # Reset stdout
    sys.stdout = sys.__stdout__ 