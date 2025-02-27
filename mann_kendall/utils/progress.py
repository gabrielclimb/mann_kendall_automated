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