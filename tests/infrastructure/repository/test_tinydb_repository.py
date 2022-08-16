import snips.infrastructure.repository.tinydb_repository as tdb
import snips.domain.snippet as snp
import snips.domain.exceptions as ex
import pytest
import os
from tempfile import gettempdir


@pytest.mark.unit
class TestTinyDbRepository:
    _TEST_DB_URI = os.path.join(gettempdir(), 'snips-db.json')

    @pytest.fixture(autouse=True)
    def _setup(self):
        self.sut = tdb.TinyDbSnipperRepository(self._TEST_DB_URI)

        print('INIT STATE IS', self.sut.get_all())
        yield
        os.remove(self._TEST_DB_URI)

    def _insert_random_snippet(self, id: str = 'drop db') -> snp.Snippet:
        e = snp.Snippet(
            id=id,
            snippet='DROP DATABASE',
            desc='drops database'
        )
        self.sut.save(e)
        return e

    def test_db_inits(self):
        assert os.path.exists(self._TEST_DB_URI)
        result = self.sut.get_all()
        print(result)

    def test_saves(self):
        e = snp.Snippet(
            id='drop db',
            snippet='DROP DATABASE',
            desc='drops database'
        )

        self.sut.save(e)
        result = self.sut.get_by_id(e.id)
        assert result

    def test_get_all_should_return_data_if_snippets_exist(self):
        self._insert_random_snippet()
        self._insert_random_snippet('create database')

        result = self.sut.get_all()
        assert len(result) == 2
        assert all(isinstance(s, snp.Snippet) for s in result)

    def test_get_all_should_return_empty_list_if_no_snippets(self):
        assert self.sut.get_all() == []

    def test_get_by_id_should_find_and_convert_to_snippet(self):
        e = self._insert_random_snippet('drop_db')
        result = self.sut.get_by_id(e.id)
        print(result)
        assert isinstance(result, snp.Snippet)

    def test_should_throw_SnippetNotFound_when_snippet_doesnt_exist(self):
        with pytest.raises(ex.SnippetNotFound):
            self.sut.get_by_id('drop database')

    def test_delete_by_id_should_remove(self):
        e = self._insert_random_snippet()
        self.sut.delete_by_id(e.id)

        with pytest.raises(ex.SnippetNotFound):
            self.sut.get_by_id(e.id)
