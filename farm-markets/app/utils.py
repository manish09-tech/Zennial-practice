import uuid

# Return a new unique identifier as a string
def new_id() -> str:
    return str(uuid.uuid4())

# Pick specified keys from a dictionary and return a new dictionary
def dict_pick(d: dict, keys: list[str]) -> dict:
    return {k: d[k] for k in keys if k in d}
