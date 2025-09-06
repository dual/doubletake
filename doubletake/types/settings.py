from typing_extensions import TypedDict, NotRequired, Callable

from doubletake.utils.meta_match import MetaMatch


class Settings(TypedDict, total=False):
    allowed: NotRequired[list[str]]
    callback: NotRequired[Callable]
    extras: NotRequired[dict[str, str]]
    idempotent: NotRequired[bool]
    known_paths: NotRequired[list[str]]
    maintain_length: NotRequired[bool]
    replace_with: NotRequired[str]
    safe_values: NotRequired[list[str]]
    use_faker: NotRequired[bool]
    meta_match: NotRequired[MetaMatch]
