from contextlib import contextmanager
import logging

logging.basicConfig(format="%(asctime)s: %(name)s: %(message)s", level=logging.INFO)

@contextmanager
def timer(task="(unnamed)"):
    start = perf_counter_ns()
    try:
        yield
        finished = perf_counter_ns()
        logger.info(f"Did {task} in {duration:0.2f} ns.")
