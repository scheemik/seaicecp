import os

from seaicecp import path

def test_list_available_models():
    """Test the `list_available_models` function."""
    # Define test cases
    ## Note: The expected output of these test cases is manually kept up to date
    test_cases = [
        {
            'institution_id': None,
            'expected_models': [
                'AWI-CM-1-1-HR',
                'AWI-CM-1-1-LR',
                'BCC-CSM2-HR',
                'CESM1-CAM5-SE-HR',
                'CESM1-CAM5-SE-LR',
                'EC-Earth3P',
                'EC-Earth3P-HR',
                'HadGEM3-GC31-HM',
                'HadGEM3-GC31-LL',
                'HadGEM3-GC31-MM',
                ],
        },
        {
            'institution_id': 'EC-Earth-Consortium',
            'expected_models': ['EC-Earth3P', 'EC-Earth3P-HR'],
        },
    ]
    for test_case in test_cases:
        actual = path.list_available_models(institution_id=test_case['institution_id'])
        assert actual == test_case['expected_models'], f"`list_available_models` failed on test case: {test_case}.\nHas the expected list in `tests/test_path/test_find_data.py` been updated?"

    # Define invalid test cases
    invalid_test_cases = [
        {
            'data_dir': 'invalid_string',
            'project': 'CMIP6',
            'activity_id': 'HighResMIP',
            'institution_id': None,
        },
        {
            'data_dir': '/seaicecp_data/bergybits/data',
            'project': 'invalid_string',
            'activity_id': 'HighResMIP',
            'institution_id': None,
        },
        {
            'data_dir': '/seaicecp_data/bergybits/data',
            'project': 'CMIP6',
            'activity_id': 'invalid_string',
            'institution_id': None,
        },
        {
            'data_dir': '/seaicecp_data/bergybits/data',
            'project': 'CMIP6',
            'activity_id': 'HighResMIP',
            'institution_id': 'invalid_string',
        },
    ]
    for invalid_test_case in invalid_test_cases:
        try:
            actual = path.list_available_models(
                data_dir = invalid_test_case['data_dir'],
                project = invalid_test_case['project'],
                activity_id = invalid_test_case['activity_id'],
                institution_id = invalid_test_case['institution_id'],
            )
        except (FileNotFoundError) as e:
            assert True, f"`list_available_models` raised an exception on invalid test case: {e}"
        else:
            assert False, f"`list_available_models` did not raise an exception on invalid test case {invalid_test_case}"
    
    # Define a list of invalid strings
    invalid_strings = [
        1234,
        3.14,
        None,
        [],
        {}
    ]
    for invalid_string in invalid_strings:
        # Test with `data_dir`
        try:
            actual = path.list_available_models(
                data_dir = invalid_string,
            )
        except (TypeError) as e:
            assert True, f"`list_available_models` raised an exception on invalid `data_dir`: {e}"
        else:
            assert False, f"`list_available_models` did not raise an exception on invalid `data_dir` {invalid_string}"
        # Test with `project`
        try:
            actual = path.list_available_models(
                project = invalid_string,
            )
        except (TypeError) as e:
            assert True, f"`list_available_models` raised an exception on invalid `project`: {e}"
        else:
            assert False, f"`list_available_models` did not raise an exception on invalid `project` {invalid_string}"
        # Test with `activity_id`
        try:
            actual = path.list_available_models(
                activity_id = invalid_string,
            )
        except (TypeError) as e:
            assert True, f"`list_available_models` raised an exception on invalid `activity_id`: {e}"
        else:
            assert False, f"`list_available_models` did not raise an exception on invalid `activity_id` {invalid_string}"
        # Test with `institution_id`
        if not isinstance(invalid_string, type(None)):
            try:
                actual = path.list_available_models(
                    institution_id = invalid_string,
                )
            except (TypeError) as e:
                assert True, f"`list_available_models` raised an exception on invalid `institution_id`: {e}"
            else:
                assert False, f"`list_available_models` did not raise an exception on invalid `institution_id` {invalid_string}"