class SnippetNotFound(Exception):
    @classmethod
    def with_message(cls, id: str):
        return cls(f"Snippet with following id: '{id}' was not found!")
