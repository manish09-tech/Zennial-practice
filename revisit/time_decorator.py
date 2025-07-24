import time

def time_decorator(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print (f"Function {func.__name__} took {end - start:.2f} seconds to execute.")
        return result
    return wrapper

@time_decorator
def time_function():
    time.sleep(10) 
    print("processing...")

time_function()