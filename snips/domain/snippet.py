from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Collection, Set, Optional
import re
import snips.domain.exceptions as ex

from pydantic import BaseModel, validator

from snips.domain.validators import Validators


class ISnippetVarsProcessor:
    OPENING_TAG: str
    CLOSING_TAG: str
    OPENING_TAG_PATTERN: str
    CLOSING_TAG_PATTERN: str
    TAG_PATTERN: str
    REMOVAL_TAG_PATTERN: str

    @classmethod
    def clean_string(cls, string: str, interpolation=False) -> str:
        """

        :param string: string that should be processed with tags indetification
        :param interpolation: wheter to replace identified vars with python interpolation placeholder
        :return: string without vars tags
        """
        dirty_arguments = re.findall(cls.TAG_PATTERN, string)

        for arg in dirty_arguments:
            clean_arg = cls._clean(arg, interpolation)
            string = string.replace(arg, clean_arg)
        return string

    @classmethod
    def _clean(cls, string: str, interpolation=False) -> str:
        clean_arg = re.sub(cls.REMOVAL_TAG_PATTERN, '', string)
        if interpolation:
            clean_arg = '{' + clean_arg + '}'
        return string.replace(string, clean_arg)

    @classmethod
    def find_and_clean(cls, string: str) -> set:
        dirty_arguments = re.findall(cls.TAG_PATTERN, string)
        return {cls._clean(s) for s in dirty_arguments}


class ArgumentTagProcessor(ISnippetVarsProcessor):
    OPENING_TAG = '<@arg>'
    CLOSING_TAG = '</@arg>'
    OPENING_TAG_PATTERN = OPENING_TAG
    CLOSING_TAG_PATTERN = '<\/@arg>'
    TAG_PATTERN = f'{OPENING_TAG_PATTERN}\s*\w+\s*{CLOSING_TAG_PATTERN}'  # '\{\s*\w+\s*}'
    REMOVAL_TAG_PATTERN = f'{OPENING_TAG_PATTERN}|{CLOSING_TAG_PATTERN}|\s+'


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
        return ArgumentTagProcessor.find_and_clean(self.snippet)

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
        snippet = ArgumentTagProcessor.clean_string(self.snippet, interpolation=True)

        return snippet.format(**{**defaults, **external_args})


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
