from dataclasses import dataclass
from enum import Enum

import snips.settings as settings
import snips.infrastructure as infra

from snips.domain import ISnippetRepository


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
class Container:
    snippet_repository: ISnippetRepository
    console_logger: infra.IConsoleLogger


def get_ioc() -> Container:
    return Container(
        repository_factory(),
        ConsoleLoggerFactory.create(settings.LOGGER_PROVIDER)
    )
