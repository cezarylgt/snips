from dataclasses import dataclass
from enum import Enum

from snips.domain import IThemeRepository
from snips.domain.themes.themes import TinyDbThemeRepository
import snips.settings as settings
import snips.infrastructure as infra

from snips.domain import ISnippetRepository
from snips.domain.service import SnippetService
from snips.infrastructure.console_logger.console_logger import ConsoleLoggerFactory


class DbProvider(str, Enum):
    JSON = 'json'


def repository_factory(provider: DbProvider = settings.CONFIG.DB_PROVIDER):
    if provider == DbProvider.JSON:
        return infra.tinydb_repository.TinyDbSnipperRepository()
    raise ValueError("Unknown configuration value for: DB_PROVIDER")


@dataclass
class IocContainer:
    repository: ISnippetRepository
    console_logger: infra.IConsoleLogger
    service: SnippetService
    theme_repository: IThemeRepository


def get_ioc() -> IocContainer:
    repository = repository_factory()
    themes = TinyDbThemeRepository(settings.THEMES_URI)
    return IocContainer(
        repository,
        ConsoleLoggerFactory.create(settings.CONFIG.FORMAT),
        SnippetService(repository),
        themes
    )
