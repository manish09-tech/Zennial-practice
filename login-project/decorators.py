import time
from logger_config import logger

def log_time(func):
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        end = time.time()
        duration = end - start
        print(f"Function {func.__name__} executed in {duration:.4f} seconds")
        logger.info(f"Function '{func.__name__}' executed in {duration:.4f} seconds")
        return result
    return wrapper