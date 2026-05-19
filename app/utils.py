"""
Utility helpers for mapping between camelCase (frontend) and snake_case (DB).
"""


def to_snake(name: str) -> str:
    """Convert camelCase to snake_case."""
    import re
    s = re.sub(r"([A-Z])", r"_\1", name).lower().lstrip("_")
    return s


def camel_to_snake_dict(d: dict) -> dict:
    """Convert all keys in a dict from camelCase to snake_case."""
    return {to_snake(k): v for k, v in d.items()}


def snake_to_camel(name: str) -> str:
    """Convert snake_case to camelCase."""
    parts = name.split("_")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])


def snake_to_camel_dict(d: dict) -> dict:
    """Convert all keys in a dict from snake_case to camelCase."""
    return {snake_to_camel(k): v for k, v in d.items()}


def model_to_camel(obj) -> dict:
    """
    Convert a SQLAlchemy model instance to a camelCase dict,
    matching what the React frontend expects.
    """
    d = {}
    for col in obj.__table__.columns:
        val = getattr(obj, col.name)
        camel_key = snake_to_camel(col.name)
        d[camel_key] = val
    return d
