import time

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
    
    def start(self):
        if self.start_time is not None:
            raise RuntimeError("Timer is already running. Call stop() before starting again.")
        self.start_time = time.perf_counter()

    def get_time(self):
        if self.start_time is None:
            raise RuntimeError("Timer is not running. Call start() before getting time.")
        return time.perf_counter() - self.start_time

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
    
    def average(self):
        avg_time = self.total_time / self.call_count if self.call_count > 0 else 0.0
        return avg_time
    
    def summary(self, print_runs=True, print_avg=True):
        print(f"\n=== Timer Summary: {self.label or 'Unnamed'} ===")
        if print_runs:
            print(f"Runs: {self.call_count}")

        print(f"Time: {self.total_time:.4f} sec")

        if print_avg:
            print(f"Average time: {self.average():.4f} sec")