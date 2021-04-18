from contextlib import contextmanager
import logging

logging.basicConfig(format="%(asctime)s: %(name)s: %(message)s", level=logging.INFO)

@contextmanager
def timer(task="(unnamed)"):
    start = perf_counter_ns()
    yield
    duration = perf_counter_ns() - start
    logger.info(f"Did {task} in {duration:0.2f} ns.")
