from __future__ import annotations
from typing import Dict, Any


def fold_object(data: Dict[str, Any], prefix: str = "") -> Dict[str, Any]:
    """
    Convert nested dictionaries into dotted-key flat dictionaries.
    Example:
        {"a": {"b": 1, "c": 2}}
    becomes:
        {"a.b": 1, "a.c": 2}
    """

    out: Dict[str, Any] = {}

    for key, value in data.items():
        full_key = f"{prefix}.{key}" if prefix else key

        if isinstance(value, dict):
            # recurse
            nested = fold_object(value, full_key)
            out.update(nested)
        else:
            out[full_key] = value

    return out


def unfold_object(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Reverse fold_object by expanding dotted keys back into nested dicts.
    """

    def _normalize_value(value: Any) -> Any:
        if isinstance(value, dict):
            return unfold_object(value)
        if isinstance(value, list):
            return [
                unfold_object(item) if isinstance(item, dict) else item
                for item in value
            ]
        return value

    def _merge_dicts(target: Dict[str, Any], incoming: Dict[str, Any]) -> Dict[str, Any]:
        for key, value in incoming.items():
            if (
                key in target
                and isinstance(target[key], dict)
                and isinstance(value, dict)
            ):
                target[key] = _merge_dicts(target[key], value)
            else:
                target[key] = value
        return target

    out: Dict[str, Any] = {}

    for key, value in data.items():
        value = _normalize_value(value)

        if "." not in key:
            existing = out.get(key)
            if isinstance(existing, dict) and isinstance(value, dict):
                out[key] = _merge_dicts(existing, value)
            else:
                out[key] = value
            continue

        parts = key.split(".")
        cursor = out

        for part in parts[:-1]:
            next_value = cursor.get(part)
            if not isinstance(next_value, dict):
                next_value = {}
                cursor[part] = next_value
            cursor = next_value

        cursor[parts[-1]] = value

    return out
