import time

# Contains utility functisons, such as logging the elapsed time.


def log_time(message: str, start_time: float):
    """
    Utility to print elapsed time with a message.
    """
    elapsed = time.time() - start_time
    print(f"{message} - Elapsed time: {elapsed:.2f} seconds.")
    return elapsed
