import snips.infrastructure.console_logger as log
import pytest

from snips.domain import Theme, Snippet
from snips.domain.themes.themes import DEFAULT_THEME


class ConsoleLoggerTestCase:
    sut: log.IConsoleLogger

    def test_log_snippets(self):
        self.sut.log_snippets(
            Snippet(
                alias='drop db',
                snippet='DROP DATABASE',
                desc='drops database',
            )
        )

    def test_print(self):
        self.sut.print('asdasda')


@pytest.mark.unit
class TestPrettyConsoleLogger(ConsoleLoggerTestCase):
    @pytest.fixture(autouse=True)
    def _setup(self):
        self.sut = log.PrettyConsoleLogger(
            DEFAULT_THEME
        )


@pytest.mark.unit
class TestTableConsoleLogger(ConsoleLoggerTestCase):
    @pytest.fixture(autouse=True)
    def _setup(self):
        self.sut = log.TableConsoleLogger(
            DEFAULT_THEME
        )
