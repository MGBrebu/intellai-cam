import time

class Timer:
    def __init__(self, label=None, verbose=True):
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

    def stop(self):
        if self.start_time is None:
            raise RuntimeError("Timer is not running. Call start() before stopping.")
        duration = time.perf_counter() - self.start_time
        self.total_time += duration
        self.call_count += 1
        self.times.append(duration)
        self.start_time = None

        if self.verbose and self.label:
            print(f"[{self.label}] Run {self.call_count}: {duration:.4f} seconds")

        return duration
    
    def average(self):
        avg_time = self.total_time / self.call_count if self.call_count > 0 else 0.0
        return avg_time
    
    def summary(self):
        print(f"\n=== Timer Summary: {self.label or 'Unnamed'} ===")
        print(f"Total runs: {self.call_count}")
        print(f"Total time: {self.total_time:.4f} sec")
        print(f"Average time: {self.average():.4f} sec")