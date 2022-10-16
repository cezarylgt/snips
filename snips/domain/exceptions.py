class SnippetNotFound(Exception):
    @classmethod
    def with_message(cls, id: str):
        return cls(f"Snippet with following id: '{id}' not found!")


class AliasAlreadyExists(Exception):

    @classmethod
    def with_message(cls, alias: str):
        return cls(f"Snippet with alias: {alias} already exists!")


class AliasInvalidCharacter(Exception):
    @classmethod
    def with_message(cls, alias: str):
        return cls(f"Alias: {alias} contains invalid characters!")


class ThemeNotFound(Exception):
    @classmethod
    def with_message(cls, name: str):
        return cls(f"Theme: '{name}' not found!")
