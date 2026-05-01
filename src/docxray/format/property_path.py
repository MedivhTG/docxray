from functools import cached_property
from typing import Any, Self


class PropertyPath(str):
    @cached_property
    def prop(self) -> str:
        return self.rsplit(".", 1)[-1]

    @cached_property
    def path_to_prop(self) -> str:
        return self.rsplit(".", 1)[0]

    @cached_property
    def links(self) -> list[str]:
        return self.split(".")

    @classmethod
    def base(cls, prop: str, path_to_prop: str = "") -> Self:
        if not path_to_prop:
            return cls(prop)
        return cls(f"{path_to_prop}.{prop}")


def safe_get_prop(
    obj: Any, prop_path: PropertyPath, default: Any = None
) -> Any:
    """Get property from object by path safely.

    Args:
        obj (Any): From python ojbect.
        prop_path (PropertyPath): Property path like `rPr.i`
        default (Any, optional): Return default if cannot get property
            on path. Defaults to None.

    Returns:
        Any: Value from property or default.
    """
    current = obj
    for link in prop_path.links:
        if not hasattr(current, link):
            return default
        current = getattr(current, link)
    return current
