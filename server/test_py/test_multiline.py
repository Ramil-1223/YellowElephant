import pytest, re

@pytest.fixture(scope = 'module')
def db_list():
    base_list = """
infobase : 4b2f4b2f-4b2f-4b2f-4b2f-4b2f4b2f4b2f
name     : base_name1
descr    : \"Description\"

infobase : d1a9d1a9-d1a9-d1a9-d1a9-d1a9d1a9d1a9
name     : base_name2
descr    : \"\"

infobase : e5c8e5c8-e5c8-e5c8-e5c8-e5c8e5c8e5c8
name     : base_name3
descr    : \"Description description\"
"""
    return base_list


@pytest.fixture(scope = 'module')
def parsed_infobases(db_list):

    pattern = (
        r"infobase\s*:\s*(?P<infobase>[a-f0-9-]{36})\s*\n"
        r"name\s*:\s*(?P<name>[^\s\n]+)\s*\n"
        # r"descr\s*:\s*.*"
        r"(?:\s*\n\s*descr\s*:\s*.*)?"
    )

    matches = re.finditer(pattern, db_list, re.MULTILINE)
    infobases = [match.groupdict() for match in matches]
    return infobases


@pytest.fixture(scope = 'module')
def dict_parsed_infobases(parsed_infobases):
    return [item['name'] for item in parsed_infobases]


@pytest.fixture(scope = 'module')
def dict_id_infobase(parsed_infobases):
    return {item['name']: item['infobase'] for item in parsed_infobases}


@pytest.fixture(scope = 'module')
def list_parsed_infobases(dict_parsed_infobases):
    return '\n'.join(dict_parsed_infobases)


def test_output_dict(parsed_infobases):
    assert parsed_infobases == [
        {'infobase': '4b2f4b2f-4b2f-4b2f-4b2f-4b2f4b2f4b2f', 'name': 'base_name1'},
        {'infobase': 'd1a9d1a9-d1a9-d1a9-d1a9-d1a9d1a9d1a9', 'name': 'base_name2'},
        {'infobase': 'e5c8e5c8-e5c8-e5c8-e5c8-e5c8e5c8e5c8', 'name': 'base_name3'}
    ]


def test_output_list(dict_parsed_infobases):
    assert dict_parsed_infobases == ['base_name1', 'base_name2', 'base_name3']


def test_output_idbase(dict_id_infobase):
    assert dict_id_infobase == {
        'base_name1': '4b2f4b2f-4b2f-4b2f-4b2f-4b2f4b2f4b2f',
        'base_name2': 'd1a9d1a9-d1a9-d1a9-d1a9-d1a9d1a9d1a9',
        'base_name3': 'e5c8e5c8-e5c8-e5c8-e5c8-e5c8e5c8e5c8'
    }


def test_output_string(list_parsed_infobases):
    assert list_parsed_infobases == "base_name1\nbase_name2\nbase_name3"