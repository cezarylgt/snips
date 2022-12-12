import pytest
import snips.domain.exceptions as ex
from snips.domain import SnippetDto
from snips.domain.service import SnippetService
from snips.infrastructure.repository.tinydb_repository import TinyDbSnipperRepository
from unittest.mock import patch, MagicMock

@pytest.mark.unit
class TestSnippetService:

    # @pytest.fixture(autouse=True)
    # def _setup(self):
    #     self.sut = SnippetService(TinyDbSnipperRepository())

    def test_create_should_raise_exception_if_overwrite_is_false_and_snippet_exists(self):
        request = SnippetDto(
            alias='test1',
            snippet='blabla',
            desc='description',
            tags=['bash']
        )
        with pytest.raises(ex.AliasAlreadyExists) as e:
            with patch.object(TinyDbSnipperRepository, 'exists') as mocked_method:
                mocked_method.return_value = True
                service = SnippetService(TinyDbSnipperRepository())
                service.create(request)

    def test_create(self):
        request = SnippetDto(
            alias='test1',
            snippet='blabla',
            desc='description',
            tags=['bash']
        )
        with patch.object(TinyDbSnipperRepository, 'exists') as mocked_method:
            mocked_method.return_value = True
            service = SnippetService(TinyDbSnipperRepository())
            service.create(request, True)


    def test_update(self): ...