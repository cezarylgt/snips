import pytest
from unittest.mock import patch
import snips.entrypoints.cli.utils as utils
from snips.domain import Snippet


@pytest.mark.unit
def test_parse_tags_converts_to_list_if_tags_is_string():
    result = utils.parse_tags("bash sql administration")
    assert result == ['bash', 'sql', 'administration']


@pytest.mark.unit
def test_parse_tags_returns_tags_as_is_if_tags_are_collection():
    result = utils.parse_tags(['1', '2', '3'])
    assert result == ['1', '2', '3']


@pytest.mark.unit
@pytest.mark.parametrize('string', [
    'key1=value1,key2=value2',
    'key1=value1,key2=value2,',
    'key1\t=value1,key2  =value2',
    '',
    None
])
def test_parse_dict(string):
    if not string:
        assert None == utils.parse_dict(string)
        return
    result = utils.parse_dict(string)
    assert result == {'key1': 'value1', 'key2': 'value2'}


@pytest.mark.unit
def test_dto_from_prompt_builds_snippet_if_snippet_is_none():
    with patch('rich.prompt.Prompt.ask') as mocked_ask:
        mocked_ask.side_effect = ['alias', 'snippet', 'description', 'bash sql', 'key1=value1,key2=value2']
        result = utils.dto_from_prompt()
        assert result.alias == 'alias'
        assert result.snippet == 'snippet'
        assert result.desc == 'description'
        assert result.tags == ['bash', 'sql']
        assert result.defaults == {'key1': 'value1', 'key2': 'value2'}


#todo: resolve set random order problem
@pytest.mark.unit
def test_prepare_command():
    snp = Snippet(
        alias='find',
        snippet="find <@arg>dir</@arg> -name '*.<@arg>ext</@arg>'",
        desc='find files by extension',
        tags=['bash']
    )
    with patch('rich.prompt.Prompt.ask') as mocked_ask:
        mocked_ask.side_effect = ['directory', 'extension']
        result = utils.prepare_command(snp)
    print(result)
    assert result == "find directory -name '*.extension'"
