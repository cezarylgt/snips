import pytest

from snips.domain.themes.themes import Theme

@pytest.mark.unit
class TestTheme:

    @pytest.fixture(autouse=True)
    def _setup(self):
        self.sut = Theme(
            name='default',
            header='red',
            text='green'
        )

    def test_if_not_alias_defined_then_should_return_text(self):
        assert self.sut.alias == self.sut.text

    def test_if_not_snippet_defined_then_should_return_text(self):
        assert self.sut.snippet == self.sut.text

    def test_if_not_desc_defined_then_should_return_text(self):
        assert self.sut.desc == self.sut.text

    def test_if_not_tags_defined_then_should_return_text(self):
        assert self.sut.tags == self.sut.text

    def test_if_not_defaults_defined_then_should_return_text(self):
        assert self.sut.defaults == self.sut.text
