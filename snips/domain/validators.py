import re
from typing import List


class Validators:

    @staticmethod
    def alias_cannot_have_white_chars(alias):
        if re.search('\s+', alias):
            raise ValueError("Aliases cannot have white chars!")
        return alias

    @staticmethod
    def snippet_cannot_be_empty(snippet: str):
        if not snippet.strip():
            raise ValueError("Snippet cannot be empty")
        return snippet

    @staticmethod
    def trim_tags(tags: List[str]):
        return [t.strip() for t in tags]
