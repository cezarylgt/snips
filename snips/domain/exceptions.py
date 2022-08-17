class SnippetNotFound(Exception):
    @classmethod
    def with_message(cls, id: str):
        return cls(f"Snippet with following id: '{id}' was not found!")


class AliasAlreadyExists(Exception):

    @classmethod
    def with_message(cls, alias: str):
        return cls(f"Snippet with alias: {alias} already exists!")


class AliasInvalidCharacter(Exception):
    @classmethod
    def with_message(cls, alias: str):
        return cls(f"Alias: {alias} contains invalid characters!")
