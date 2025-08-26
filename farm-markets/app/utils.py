import uuid
from datetime import datetime

# Returns new unique identifier as a string
def new_id() -> str:
    return str(uuid.uuid4())

# Returns the current date and time
def now() -> datetime:
    return datetime.now()

# Returns a new dictionary containing only the specified keys from the original dictionary
def dict_pick(d: dict, keys: list[str]) -> dict:
    return {k: d[k] for k in keys if k in d}