import re


def replace_times(path: str, start: int, add: int):
    with open(path, encoding='utf-8') as f:
        lines = f.readlines()[start:]

    patter = '\d\d\.'
    corr = []
    for l in lines:
        found = re.findall(patter, l)[0]

        corr.append( l.replace(found, f"{int(found[:2]) + add}.").strip())
    print()
    for l in corr :
        print(l)

def test_replace():

    replace_times('/home/cezaryl/dev/python/new-snips/demo/create-edit-run.cast',145, 31)