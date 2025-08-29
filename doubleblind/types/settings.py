from typing_extensions import TypedDict, NotRequired, Callable


class Settings(TypedDict, total=False):
    allowed: NotRequired[list[str]]
    callback: NotRequired[Callable]
    extras: NotRequired[list[str]]
    known_paths: NotRequired[list[str]]
    maintain_length: NotRequired[bool]
    replace_with: NotRequired[str]
    use_faker: NotRequired[bool]
