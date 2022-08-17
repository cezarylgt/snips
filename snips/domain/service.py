import abc

from snips.domain import ISnippetRepository, SnippetDto, Snippet
import snips.domain.exceptions as ex


class SnippetService(abc.ABC):

    def __init__(self, repository: ISnippetRepository):
        self.repository = repository

    def create(self, request: SnippetDto, overwrite=False) -> Snippet:
        if overwrite is False:
            if self.repository.exists(request.alias):
                raise ex.AliasAlreadyExists.with_message(request.alias)
        return self.repository.save(request.to_entity())

    def update(self, request: SnippetDto) -> Snippet:
        snippet = self.repository.get_by_id(request.alias)
        request.update_entity(snippet)
        return self.repository.save(snippet)
