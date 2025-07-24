def log_action(function):
    def wrapper(*args, **kwargs):
        print (f"Calling function '{function.__name__}' with arguments: {args} and keyword arguments: {kwargs}")
        result = function(*args, **kwargs)
        print(f"Function '{function.__name__}' returned: {result}")
        return result
    return wrapper

@log_action
def enroll_student(name):
    """Enroll a student in a school."""
    print (f"Enrolling student: {name}")

enroll_student("Harshit")