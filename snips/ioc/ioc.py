from dataclasses import dataclass
from enum import Enum

from snips.settings import CONFIG
import snips.infrastructure as infra

from snips.domain import ISnippetRepository
from snips.domain.service import SnippetService
from snips.infrastructure.console_logger.console_logger import ConsoleLoggerFactory


class DbProvider(str, Enum):
    JSON = 'json'


def repository_factory(provider: DbProvider = CONFIG.DB_PROVIDER):
    if provider == DbProvider.JSON:
        return infra.tinydb_repository.TinyDbSnipperRepository()
    raise ValueError("Unknown configuration value for: DB_PROVIDER")


@dataclass
class IocContainer:
    repository: ISnippetRepository
    console_logger: infra.IConsoleLogger
    service: SnippetService


def get_ioc() -> IocContainer:
    repository = repository_factory()
    return IocContainer(
        repository,
        ConsoleLoggerFactory.create(CONFIG.FORMAT),
        SnippetService(repository)
    )
