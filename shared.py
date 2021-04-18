from contextlib import contextmanager
import logging
from time import perf_counter_ns

logging.basicConfig(format="%(asctime)s: %(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

@contextmanager
def timer(task="(unnamed)"):
    start = perf_counter_ns()
    yield
    duration = perf_counter_ns() - start
    logger.info(f"Did {task} in {duration:0.2f} ns ({duration/1e6:0.2f} ms).")
