from dataclasses import dataclass


@dataclass
class Book:
    """Book object with title and author information."""

    title: str
    author: str

    short_title: str = None
    last_name: str = None

    def __post_init__(self):
        self.short_title = self.title.split(":")[0]
        self.last_name = self.author.split(",")[0]

    def __repr__(self) -> str:
        return f"{self.last_name}: {self.short_title}"
