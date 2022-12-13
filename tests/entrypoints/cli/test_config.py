import os
from typing import Any

from typer.testing import CliRunner
from snips.entrypoints.cli.cli import app, LongArgs, ShortArgs
import pytest
import snips.domain as dm
import snips.settings as settings
import pyperclip
import ast


def dsr(s: str) -> Any:
    return ast.literal_eval(s)


def rpl(s: str):
    return '[{}]'.format(s.replace("}\n{", "},{"))


runner = CliRunner()


# todo: assert results
@pytest.mark.e2e
class TestConfigCli:
    def test_cli_config_show_should_print_configuration(self):
        result = runner.invoke(app, ['config', 'show'])
        assert result.exit_code == 0
        config = dsr(result.stdout)
        assert all(x in config for x in ['FORMAT', 'DB_URI', 'DB_PROVIDER'])
        print(result.stdout)

    def test_cli_config_set_should_set_format(self):
        result = runner.invoke(app, ['config', 'set', 'format', 'table'])
        assert result.exit_code == 0
        result = runner.invoke(app, ['config', 'show'])
        config = dsr(result.stdout)
        print(result.stdout)
        assert config['FORMAT'] == 'table'

    def test_cli_config_get_path_should_print_path_of_config_file(self):
        result = runner.invoke(app, ['config', 'path'])
        assert result.exit_code == 0


@pytest.mark.e2e
class TestCli:

    @pytest.fixture(autouse=True)
    def _setup(self):
        # set eniron
        settings.CONFIG.DB_URI = '/home/cezaryl/test-db.json'
        result = runner.invoke(app, ['config', 'set', 'format', 'json'])
        assert result.exit_code == 0

        app.repository.remove_all()
        app.service.create(
            dm.SnippetDto(
                alias='test1',
                snippet='ls <@arg>directory</@arg>',
                desc='description',
                tags=['bash'],
                defaults={'directory': 'YOUR HOME DIRECTORY'}
            )
        )
        app.service.create(
            dm.SnippetDto(
                alias='test2',
                snippet='ls <@arg>directory</@arg>',
                desc='description',
                tags=['bash', 'sql']
            )
        )

        self.snippet1 = app.repository.get_by_id('test1')
        self.snippet2 = app.repository.get_by_id('test2')
        assert app.repository.get_all()
        yield
        app.repository.remove_all()

    def test_cli_show_by_alias(self):
        result = runner.invoke(app, ['show', 'test1'])
        assert result.exit_code == 0
        assert dsr(result.stdout) == self.snippet1.dict()

    def test_cli_ls_should_print_all_snippets(self):
        result = runner.invoke(app, ['ls'])
        assert result.exit_code == 0
        objects = dsr(rpl(result.stdout))
        assert objects == [self.snippet1.dict(), self.snippet2.dict()]

    def test_cli_ls_with_tags_should_print_snippets_only_containing_given_tags(self):
        result = runner.invoke(app, ['ls', '--tags', 'sql', '--tags-mode', 'any'])
        assert result.exit_code == 0
        objects = dsr(rpl(result.stdout))
        assert objects == [self.snippet2.dict()]

    def test_cli_get_should_copy_snippet_to_clipboard_with_defaults_and(self):
        result = runner.invoke(app, ['get', 'test1'])
        print(result.stdout)
        assert result.exit_code == 0
        assert self.snippet1.parse_command() in result.stdout
        assert pyperclip.paste() == self.snippet1.parse_command()

    def test_cli_get_with_raw_option_should_copy_to_clipboard_without_arg_interpolation(self):
        result = runner.invoke(app, ['get', 'test1', '--raw'])
        print(result.stdout)
        assert result.exit_code == 0
        assert pyperclip.paste() == self.snippet1.snippet

    def test_cli_rm_removes_permanently(self):
        result = runner.invoke(app, ['rm', 'test1'])
        assert result.exit_code == 0
        assert not app.repository.exists('test1')

    @pytest.mark.parametrize(
        'arg_names', [LongArgs, ShortArgs]
    )
    def test_cli_add_should_add_new_snippet(self, arg_names):
        result = runner.invoke(app, ['add',
                                     arg_names.alias, 'test3',
                                     arg_names.snippet, 'some-command',
                                     arg_names.desc, '3rd snippet',
                                     arg_names.tags, 'python',
                                     arg_names.tags, 'bash'
                                     ]
                               )
        assert result.exit_code == 0
        created = app.repository.get_by_id('test3')
        assert created.alias == 'test3'
        assert created.snippet == 'some-command'
        assert created.desc == '3rd snippet'
        assert created.tags == ['python', 'bash']

        print(result)

    @pytest.mark.parametrize(
        'arg_names', [LongArgs, ShortArgs]
    )
    def test_cli_add_with_file_should_read_file_content_and_assing_to_snippet(self, arg_names):
        test_path = 'test-file.txt'
        with open(test_path, 'w') as f:
            f.write('snippet read from file')

        try:
            result = runner.invoke(app, ['add',
                                         arg_names.file, test_path,
                                         arg_names.alias, 'test3',
                                         arg_names.desc, '3rd snippet',
                                         arg_names.tags, 'python',
                                         arg_names.tags, 'bash'
                                         ]
                                   )
            assert result.exit_code == 0
            created = app.repository.get_by_id('test3')
            assert created.alias == 'test3'
            assert created.snippet == 'snippet read from file'
            assert created.desc == '3rd snippet'
            assert created.tags == ['python', 'bash']
        except Exception as e:
            raise e
        finally:
            os.remove(test_path)

    def test_cli_add_should_raise_exception_if_alias_already_exists(self):
        result = runner.invoke(app, ['add',
                                     LongArgs.alias, 'test2',
                                     LongArgs.snippet, 'some-command',
                                     LongArgs.desc, '3rd snippet',
                                     LongArgs.tags, 'python',
                                     LongArgs.tags, 'bash'
                                     ]
                               )
        assert result.exit_code == 1
        print(result)
        print(result.stdout)

    @pytest.mark.parametrize(
        'arg_names', [LongArgs, ShortArgs]
    )
    def test_cli_edit_should_edit(self, arg_names):
        result = runner.invoke(app, ['edit',
                                     'test1',
                                     arg_names.alias, 'test1',
                                     arg_names.snippet, 'some-command',
                                     arg_names.desc, 'edited description',
                                     arg_names.tags, 'sql',
                                     ]
                               )
        assert result.exit_code == 0
        modified = app.repository.get_by_id('test1')
        assert modified.snippet == 'some-command'
        assert modified.desc == 'edited description'
        assert modified.tags == ['sql']

    def test_run_with_provided_arg(self):
        result = runner.invoke(app, ['run', 'test1', '--args', 'directory=.'])
        assert result.exit_code == 0
