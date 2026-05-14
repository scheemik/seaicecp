from cdo import CDOException

from seaicecp.dataset import field_mean

def test_get_field_mean():
    """Test the `get_field_mean` function."""
    # Define test cases
    ## Note: The expected output of these test cases is manually kept up to date
    test_cases = [
        {
            'dataset': 'data/NWP_cdo_CLI_areacello_Ofx_EC-Earth3P-HR_highres-future_r2i1p2f1_gn.nc',
            'variable_id': 'areacello',
            'expected_means': [
                1.3731426e+08,
                ],
        },
    ]
    for test_case in test_cases:
        actual = list(field_mean.get_field_mean(test_case['dataset'])[test_case['variable_id']].values.flatten())
        assert actual == test_case['expected_means'], f"`get_field_mean` failed on test case: {test_case}.\nExpected means: {test_case['expected_means']}\nActual means: {actual}"

    # Define invalid test cases
    invalid_test_cases = [
        {
            'dataset': 'invalid_dataset',
        },
    ]
    for invalid_test_case in invalid_test_cases:
        try:
            actual = field_mean.get_field_mean(
                dataset = invalid_test_case['dataset'],
            )
        except (CDOException) as e:
            assert True, f"`get_field_mean` raised an exception on invalid test case: {e}"
        else:
            assert False, f"`get_field_mean` did not raise an exception on invalid test case {invalid_test_case}"
    
    # Define a list of invalid datasets
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
            actual = field_mean.get_field_mean(
                dataset = invalid_string,
            )
        except (TypeError) as e:
            assert True, f"`get_field_mean` raised an exception on invalid `dataset`: {e}"
        else:
            assert False, f"`get_field_mean` did not raise an exception on invalid `dataset` {invalid_string}"
        # Test with `save_as`
        if not isinstance(invalid_string, type(None)):
            try:
                actual = field_mean.get_field_mean(
                    dataset = test_cases[0]['dataset'],
                    save_as = invalid_string,
                )
            except (TypeError) as e:
                assert True, f"`get_field_mean` raised an exception on invalid `save_as`: {e}"
            else:
                assert False, f"`get_field_mean` did not raise an exception on invalid `save_as` {invalid_string}"