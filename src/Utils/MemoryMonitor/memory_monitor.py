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
    def __init__(self, interval=300):
        self.interval = interval
        self.process = psutil.Process(os.getpid())
        self.monitor_thread = threading.Thread(target=self.monitor_memory_usage)
        self.monitor_thread.daemon = True

    def start(self):
        self.monitor_thread.start()

    def monitor_memory_usage(self):
        max_memory = 0

        while True:
            current_memory = self.process.memory_info().rss  # Get the current memory usage in bytes
            max_memory = max(max_memory, current_memory)
            print(f"Current memory usage: {current_memory / 1024 / 1024:.2f} MB")
            print(f"Max memory usage: {max_memory / 1024 / 1024:.2f} MB")

            # Show memory usage of individual Python objects
            tracked_objects = [
                # Add objects to be tracked for memory usage here
            ]

            print("Memory usage by individual objects:")
            for obj in tracked_objects:
                obj_name = str(obj.__class__.__name__)
                obj_size = get_deep_size(obj) / 1024 / 1024
                print(f"{obj_name}: {obj_size:.2f} MB")

            time.sleep(self.interval)
