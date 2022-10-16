from snips.settings import Configuration


def test_partial_init():
    di = dict(TEXT_STYLE='blue orange')
    config = Configuration(**di)
    assert config.TEXT_STYLE == 'blue orange'
