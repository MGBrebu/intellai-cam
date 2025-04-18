import time

# CLASS: General performance timer
# Remembers runs, total time, and average time
class Timer:
    def __init__(self, label=None, verbose=True):
        if label is None:
            Timer._counter += 1
            label = f"Timer-{Timer._counter}"
        self.label = label
        self.verbose = verbose
        self.start_time = None
        self.total_time = 0.0
        self.call_count = 0
        self.times = []
    
    # DEF: Start a timer
    def start(self):
        if self.start_time is not None:
            raise RuntimeError("Timer is already running. Call stop() before starting again.")
        self.start_time = time.perf_counter()

    # DEF: Get elapsed time since start
    def get_time(self):
        if self.start_time is None:
            raise RuntimeError("Timer is not running. Call start() before getting time.")
        return time.perf_counter() - self.start_time

    # DEF: Stop the timer and return elapsed time
    def stop(self):
        if self.start_time is None:
            raise RuntimeError("Timer is not running. Call start() before stopping.")
        duration = time.perf_counter() - self.start_time
        self.total_time += duration
        self.call_count += 1
        self.times.append(duration)
        self.start_time = None

        if self.verbose and self.label:
            print(f"[T:{self.label}] Run {self.call_count}: {duration:.4f} seconds")

        return duration
    
    # DEF: Get the average time of all runs
    def average(self):
        avg_time = self.total_time / self.call_count if self.call_count > 0 else 0.0
        return avg_time
    
    # DEF: Print a summary of the timer object
    # Includes call count, total time, and average time
    def summary(self, print_runs=True, print_avg=True):
        print(f"\n=== Timer Summary: {self.label or 'Unnamed'} ===")
        if print_runs:
            print(f"Runs: {self.call_count}")

        print(f"Time: {self.total_time:.4f} sec")

        if print_avg:
            print(f"Average time: {self.average():.4f} sec")