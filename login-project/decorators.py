import time

def log_time(func):
    async def wrapper(*args, **kwargs):
        start = time.time()
        result = await func(*args, **kwargs)
        end = time.time()
        print(f"Function {func.__name__} executed in {end - start} seconds")
        return result
    return wrapper