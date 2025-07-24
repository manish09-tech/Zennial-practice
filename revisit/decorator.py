def decorate(actual_func):
    def wrapper(*args, **kwargs):
        print("Before calling the actual function")
        result = actual_func(*args, **kwargs)
        print("After calling the actual function")
        return result
    return wrapper
    
@decorate
def function(x, y):
    """An example function that adds two numbers."""
    print(f"Example function called with x={x}, y={y}")

function(1, 2)