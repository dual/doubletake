from typing_extensions import TypedDict, NotRequired, Callable


class Settings(TypedDict, total=False):
    allowed: NotRequired[list[str]]
    callback: NotRequired[Callable]
    extras: NotRequired[list[str]]
    idempotent: NotRequired[bool]
    known_paths: NotRequired[list[str]]
    maintain_length: NotRequired[bool]
    replace_with: NotRequired[str]
    safe_values: NotRequired[list[str]]
    use_faker: NotRequired[bool]
