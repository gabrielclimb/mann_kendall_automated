
import streamlit as st


def print_progress_bar(
    iteration: int,
    total: int,
    prefix: str = "",
    suffix: str = "",
    decimals: int = 1,
    length: int = 100,
    fill: str = "█",
    printEnd: str = "\r",
) -> None:
    """
    Prints a progress bar in the terminal.

    Args:
        iteration (int): Current iteration.
        total (int): Total iterations.
        prefix (str, optional): Prefix string. Defaults to "".
        suffix (str, optional): Suffix string. Defaults to "".
        decimals (int, optional): Number of decimals in the percent complete. Defaults to 1.
        length (int, optional): Character length of the progress bar. Defaults to 100.
        fill (str, optional): Bar fill character. Defaults to "█".
        printEnd (str, optional): End character (e.g., "\r", "\r\n"). Defaults to "\r".
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    progress_bar = fill * filledLength + "-" * (length - filledLength)
    print(f"\r{prefix} |{progress_bar}| {percent}%% {suffix}", end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


class StreamlitProgressTracker:
    """Enhanced progress tracking for Streamlit applications."""
    
    def __init__(self, total_steps: int, title: str = "Processing"):
        self.total_steps = total_steps
        self.current_step = 0
        self.title = title
        self.progress_bar = st.progress(0)
        self.status_text = st.empty()
        
    def update(self, step_name: str, increment: int = 1):
        """Update progress with step name."""
        self.current_step += increment
        progress = min(self.current_step / self.total_steps, 1.0)
        
        self.progress_bar.progress(progress)
        self.status_text.text(f"{self.title}: {step_name} ({self.current_step}/{self.total_steps})")
        
    def complete(self, final_message: str = "Complete!"):
        """Mark progress as complete."""
        self.progress_bar.progress(1.0)
        self.status_text.text(final_message)
        
    def cleanup(self):
        """Remove progress indicators."""
        self.progress_bar.empty()
        self.status_text.empty()