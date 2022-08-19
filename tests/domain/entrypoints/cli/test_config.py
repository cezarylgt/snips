import os
from typing import Any

from typer.testing import CliRunner
from snips.entrypoints.cli.cli import app, LongArgs, ShortArgs
import pytest
import snips.domain as dm
import snips.settings as settings
import pyperclip
import ast

runner = CliRunner()


@pytest.mark.e2e
class TestConfigCli:
    def test_show_prints_configuration(self):
        result = runner.invoke(app, ['config', 'show'])
        print(result.stdout)
        assert result.exit_code == 0
        print(result)

    def test_set_format(self):
        result = runner.invoke(app, ['config', 'set', 'format', 'table'])
        assert result.exit_code == 0

    def test_get_path_returns_path_to_config(self):
        result = runner.invoke(app, ['config', 'path'])
        assert result.exit_code == 0


def dsr(s: str) -> Any:
    return ast.literal_eval(s)


def rpl(s: str):
    return '[{}]'.format(s.replace("}\n{", "},{"))


@pytest.mark.e2e
class TestCli:

    @pytest.fixture(autouse=True)
    def _setup(self):
        # set eniron
        result = runner.invoke(app, ['config', 'set', 'format', 'json'])
        assert result.exit_code == 0

        app.repository.remove_all()
        app.service.create(
            dm.SnippetDto(
                alias='test1',
                snippet='ls <@arg>directory</@arg>',
                desc='description',
                tags=['bash']
            )
        )
        app.service.create(
            dm.SnippetDto(
                alias='test2',
                snippet='ls <@arg>directory</@arg>',
                desc='description',
                tags=['bash']
            )
        )

        self.snippet1 = app.repository.get_by_id('test1')
        self.snippet2 = app.repository.get_by_id('test2')
        assert app.repository.get_all()
        yield
        app.repository.remove_all()

    def test_show_by_alias(self):
        result = runner.invoke(app, ['show', 'test1'])
        assert result.exit_code == 0
        assert dsr(result.stdout) == self.snippet1.dict()

    def test_ls_should_print_all_snippets(self):
        result = runner.invoke(app, ['ls'])
        assert result.exit_code == 0
        objects = dsr(rpl(result.stdout))
        assert len(objects) == 2
        assert objects == [self.snippet1.dict(), self.snippet2.dict()]

    def test_get_with_raw_option_should_copy_to_clipboard_without_arg_interpolation(self):
        result = runner.invoke(app, ['get', 'test1', '--raw'])
        print(result.stdout)
        assert result.exit_code == 0
        assert pyperclip.paste() == self.snippet1.snippet

    def test_delete_removes_permanently(self):
        result = runner.invoke(app, ['rm', 'test1'])
        assert result.exit_code == 0
        assert not app.repository.exists('test1')

    @pytest.mark.parametrize(
        'arg_names', [LongArgs, ShortArgs]
    )
    def test_add(self, arg_names):
        result = runner.invoke(app, ['add',
                                     arg_names.alias, 'test3',
                                     arg_names.snippet, 'some-command',
                                     arg_names.desc, '3rd snippet',
                                     arg_names.tags, 'python',
                                     arg_names.tags, 'bash'
                                     ]
                               )
        assert result.exit_code == 0
        modified = app.repository.get_by_id('test3')
        assert modified.alias == 'test3'
        assert modified.snippet == 'some-command'
        assert modified.desc == '3rd snippet'
        assert modified.tags == ['python', 'bash']

        print(result)

    @pytest.mark.parametrize(
        'arg_names', [LongArgs, ShortArgs]
    )
    def test_edit(self, arg_names):
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

    def test_run_with_rpovided_arg(self):
        result = runner.invoke(app, ['run', 'test1', '--args', 'directory=.'])
        assert result.exit_code == 0
