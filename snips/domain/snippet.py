from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Collection, Set, Optional
import re
import snips.domain.exceptions as ex

from pydantic import BaseModel, validator

from snips.domain.validators import Validators


def remove_argument_tags(arguments: List[str]) -> set:
    replace = lambda x: re.sub('\{|}|\s*', '', x)
    return {replace(s) for s in arguments}


@dataclass
class Snippet:
    alias: str
    snippet: str
    desc: str
    tags: List[str] = None
    defaults: dict = None
    created_at: datetime = None
    updated_at: datetime = None

    def dict(self):
        return asdict(self)

    def get_arguments(self) -> set[str]:
        return remove_argument_tags(re.findall('\{\s*\w+\s*}', self.snippet))

    def all_arguments_have_defaults(self):
        if not self.defaults:
            return False

        self.get_arguments()

    def get_missing_default_arguments(self, external_arguments: Collection[str] = None) -> Set[str]:
        if external_arguments is None:
            external_arguments = set()
        arguments = self.get_arguments()
        df = self.defaults or dict()
        return arguments.difference(set(df.keys()).union(set(external_arguments)))

    def parse_command(self, external_args: dict = None):
        if not external_args:
            external_args = dict()

        defaults = self.defaults or dict()

        return self.snippet.format(**{**defaults, **external_args})


# todo: trim everything
class SnippetDto(BaseModel):
    alias: str
    snippet: str
    desc: Optional[str]
    tags: List[str] = None
    defaults: dict = None

    _alias_cannot_have_white_chars = validator('alias')(Validators.alias_cannot_have_white_chars)
    _snippet_cannot_be_empty = validator('snippet')(Validators.snippet_cannot_be_empty)

    def __init__(self, **data):
        if data.get('tags'):
            data['tags'] = Validators.trim_tags(data.get('tags'))

        super(SnippetDto, self).__init__(**data)


    def to_entity(self) -> Snippet:
        return Snippet(
            self.alias,
            self.snippet,
            self.desc,
            self.tags,
            self.defaults
        )

    def update_entity(self, e: Snippet):
        e.alias = self.alias
        e.snippet = self.snippet
        e.desc = self.desc
        e.tags = self.tags
        e.defaults = self.defaults
