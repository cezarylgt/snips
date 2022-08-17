import pytest

import snips.domain as dm
import snips.domain.exceptions as ex


@pytest.mark.unit
class TestSnippet:

    def _example(self) -> dm.Snippet:
        return dm.Snippet('ex', 'execute {filename} -p {directory} -f {directory}', 'does something',
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

    def test_alias_validator(self):
        with pytest.raises(ex.AliasInvalidCharacter):
            request = dm.SnippetDto(
                alias='alias with white char',
                snippet='bla bla',
                desc='',
            )
