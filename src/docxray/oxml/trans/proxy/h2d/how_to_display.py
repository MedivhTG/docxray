from typing import Generic, TypeVar

from .resolver import Resolver

RESOLVER_T = TypeVar("RESOLVER_T", bound=Resolver)


class How2Display(Generic[RESOLVER_T]):
    def __init__(self, resolver: RESOLVER_T) -> None:
        self._resolver = resolver
