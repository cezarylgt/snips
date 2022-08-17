from dataclasses import dataclass
from enum import Enum

import snips.settings as settings
import snips.infrastructure as infra

from snips.domain import ISnippetRepository
from snips.domain.service import SnippetService


class DbProvider(str, Enum):
    JSON = 'json'


def repository_factory(provider: DbProvider = settings.DB_PROVIDER):
    if provider == DbProvider.JSON:
        return infra.tinydb_repository.TinyDbSnipperRepository()
    raise ValueError("Unknown configuration value for: DB_PROVIDER")


class ConsoleLoggerProvider(str, Enum):
    POOR = 'poor'
    JSON = 'json'
    PRETTY = 'pretty'


class ConsoleLoggerFactory:
    _mapping = {
        ConsoleLoggerProvider.POOR: infra.PrettyConsoleLogger,
        ConsoleLoggerProvider.JSON: infra.JsonConsoleLogger,
        ConsoleLoggerProvider.PRETTY: infra.PrettyConsoleLogger
    }

    @staticmethod
    def create(logger_provider: ConsoleLoggerProvider) -> infra.IConsoleLogger:
        return ConsoleLoggerFactory._mapping[logger_provider]()


@dataclass
class IocContainer:
    repository: ISnippetRepository
    console_logger: infra.IConsoleLogger
    service: SnippetService


def get_ioc() -> IocContainer:
    repository = repository_factory()
    return IocContainer(
        repository,
        ConsoleLoggerFactory.create(settings.LOGGER_PROVIDER),
        SnippetService(repository)
    )
