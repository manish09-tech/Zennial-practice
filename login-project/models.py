from database import collection
from auth import hash_password, verify_password
from datetime import datetime

def is_password_reused(new_pwd, past_pwds):
    from auth import pwd_context
    for old_pwd in past_pwds:
        if pwd_context.verify(new_pwd, old_pwd):
            return True
    return False

def update_password(email, new_hashed_password):
    collection.update_one(
        {"email": email},
        {"$set": {
            "password": new_hashed_password,
            "last_password_change": datetime.now()
        },
        "$push": {
            "password_history": {
                "$each": [new_hashed_password],
                "$slice": -5
            }
        }}
    )
