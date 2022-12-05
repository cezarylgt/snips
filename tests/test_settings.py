from snips.settings import Configuration


def test_partial_init():
    di = dict(TEXT_STYLE='blue orange')
    config = Configuration(**di)
    assert config.TEXT_STYLE == 'blue orange'

def test_string_interpolation():
    s = "mysupertextfile_{context_execution_date}"
    context = {
        'context_execution_date': 'aaaaa'
    }

    print(s.format(**context))

"""


"""