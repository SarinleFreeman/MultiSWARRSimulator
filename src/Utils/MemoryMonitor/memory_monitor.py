import os
import time
import psutil
import threading
from objsize import get_deep_size


class MemoryMonitor:
    """
    The goal of this class is to monitor the memory usage of your program. It will
    inform a user at set intervals the maximum, current and object memory being used.
    """

    def __init__(self, program_name, interval=300):
        self.interval = interval
        self.process = psutil.Process(os.getpid())
        self.monitor_thread = threading.Thread(target=self.monitor_memory_usage)
        self.monitor_thread.daemon = True
        self.name = program_name

    def start(self):
        print(f"Starting memory monitor for {self.name}...")
        self.monitor_thread.start()

    def monitor_memory_usage(self):
        max_memory = 0
        while True:
            current_memory = self.process.memory_info().rss  # Get the current memory usage in bytes
            max_memory = max(max_memory, current_memory)
            print(f"Current memory usage: {current_memory / 1024 / 1024:.2f} MB")
            print(f"Max memory usage: {max_memory / 1024 / 1024:.2f} MB")

            time.sleep(self.interval)
