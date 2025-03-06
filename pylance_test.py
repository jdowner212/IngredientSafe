from typing import TypedDict, Literal

# TypedDict is a Pylance-supported feature
class UserConfig(TypedDict):
    name: str
    age: int
    status: Literal["active", "inactive"]

def process_user(config: UserConfig) -> str:
    return f"{config['name']} is {config['age']} years old"

# This should show Pylance-specific type checking
test_config = {
    "name": "John",
    "age": "25",  # This should show a type error
    "status": "pending"  # This should show a literal type error
} 