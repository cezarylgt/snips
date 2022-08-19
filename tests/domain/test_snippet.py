import pytest
from pydantic import ValidationError

import snips.domain as dm
import snips.domain.snippet as sn


class TestArgumentTagProcessor:

    def test_remove_arg_tag(self):
        string = f'{sn.ArgumentTagProcessor.OPENING_TAG} argument {sn.ArgumentTagProcessor.CLOSING_TAG} -f {sn.ArgumentTagProcessor.OPENING_TAG} second {sn.ArgumentTagProcessor.CLOSING_TAG}'
        result = sn.ArgumentTagProcessor.clean_string(string)
        assert result == 'argument -f second'

    def test_remove_arg_tags_with_nested_qoutes(self):
        # string = f'find {sn.ArgumentTagProcessor.OPENING_TAG}dir{sn.ArgumentTagProcessor.CLOSING_TAG} -f {sn.ArgumentTagProcessor.OPENING_TAG} second {sn.ArgumentTagProcessor.CLOSING_TAG}'
        string = "find <@arg>dir</@arg> -name '*.<@arg>ext</@arg>'"
        result = sn.ArgumentTagProcessor.clean_string(string, interpolation=True)


@pytest.mark.unit
class TestSnippet:

    def _example(self) -> dm.Snippet:
        return dm.Snippet('ex', 'execute <@arg>filename  </@arg> -p <@arg>directory</@arg> -f <@arg>directory</@arg>',
                          'does something',
                          defaults={'filename': '/home/.vimrc', 'directory': 'home'}
                          )

    def test_get_arguments_should_return_all_args_contained_in_snippet(self):
        snippet = self._example()
        arguments = snippet.get_arguments()
        print(arguments)

        assert type(arguments) == set
        assert len(arguments) == 2
        assert arguments == {'filename', 'directory'}

    @pytest.mark.parametrize(
        'defaults, expected', [
            (dict(filename='/home', directory='/home'), set()),
            (dict(filename='.vimrc'), {'directory'}),
            (dict(), {'filename', 'directory'}),
        ]
    )
    def test_get_missing_arguments_should_return_only_args_not_contained_in_defaults(self,
                                                                                     defaults, expected
                                                                                     ):
        snippet = self._example()
        snippet.defaults = defaults
        missing = snippet.get_missing_default_arguments()
        assert missing == expected

    @pytest.mark.parametrize(
        'external, expected', [
            (dict(filename='/home', directory='/home'), set()),
            (dict(filename='.vimrc'), {'directory'}),
            (dict(), {'filename', 'directory'}),
        ]
    )
    def test_get_missing_arguments_with_external_should_ony_return_difference(self,
                                                                              external, expected
                                                                              ):
        snippet = self._example()
        snippet.defaults = None
        result = snippet.get_missing_default_arguments(external.keys())
        assert result == expected

    def test_parse_command_when_all_defaults_provided(self):
        cmd = self._example().parse_command()
        assert cmd == 'execute /home/.vimrc -p home -f home'

    def test_parse_command_when_external_args_override_defaults(self):
        snippet = self._example()
        cmd = snippet.parse_command(dict(filename='external-value'))
        assert cmd == 'execute external-value -p home -f home'

    def test_parse_command_when_not_enough_args_provided(self):
        snippet = self._example()
        snippet.defaults = None
        with pytest.raises(KeyError):
            snippet.parse_command(dict(filename='external-value'))


@pytest.mark.unit
class TestCreateSnippetDto:

    def test_alias_validator_during_initialization(self):
        with pytest.raises(ValidationError):
            request = dm.SnippetDto(
                alias='alias with white char',
                snippet='bla bla',
                desc='',
            )

    def test_snippet_cannot_be_blank(self):
        with pytest.raises(ValidationError) as err:
            request = dm.SnippetDto(
                alias='alias',
                snippet=' ',
                desc='',
            )

        exc: ValidationError = err.value
        assert 'Snippet cannot be empty' in exc.errors()[0]['msg']

    def test_trims_tags_after_init(self):
        request = dm.SnippetDto(
            alias='alias',
            snippet='bla bla',
            desc='',
            tags=['python   ', ' bash']
        )
        assert set(request.tags) == {'python', 'bash'}

    def test_drop_empty_tags_after_init(self):
        request = dm.SnippetDto(
            alias='alias',
            snippet='bla bla',
            desc='',
            tags=['python   ', ' bash', '', '']
        )
        assert set(request.tags) == {'python', 'bash'}
