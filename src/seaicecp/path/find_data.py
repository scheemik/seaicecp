import os
import glob
import warnings
from datetime import datetime

from seaicecp.verify import verify_path

"""
The functions in this module assume the files are organized in the default fashion of `esgpull`.
This has the general structure as shown below.

/seaicecp_data/bergybits/
    ├── data
    │   └── CMIP6
    │       └── HighResMIP
    │           ├── AWI
    │           │   ├── AWI-CM-1-1-HR
    │           │   │   ├── hist-1950
    │           │   │   │   └── r1i1p1f2
    │           │   │   │       └── Ofx
    │           │   │   │           └── areacello
    │           │   │   │               └── gn
    │           │   │   │                   └── v20170825
    │           │   │   │                       └── areacello_Ofx_AWI-CM-1-1-HR_hist-1950_r1i1p1f2_gn.nc
    │           │   └── AWI-CM-1-1-LR
    │           │       ├── ...
    │           ├── ...
    │           ├── EC-Earth-Consortium
    │           │   ├── EC-Earth3P
    │           │   │   └── ...
    │           │   └── EC-Earth3P-HR
    │           │       └── hist-1950
    │           │           ├── r1i1p2f1
    │           │           │   └── SImon
    │           │           │       ├── siage
    │           │           │       │   └── gn
    │           │           │       │       └── v20181212
    │           │           │       │           ├── siage_SImon_EC-Earth3P-HR_hist-1950_r1i1p2f1_gn_195001-195012.nc
    │           │           │       │           ├── ...
    │           │           │       │           └── siage_SImon_EC-Earth3P-HR_hist-1950_r1i1p2f1_gn_201401-201412.nc
    │           │           │       ├── siconc
    │           │           │       │   └── gn
    │           │           │       │       └── v20181212
    │           │           │       │           ├── siconc_SImon_EC-Earth3P-HR_hist-1950_r1i1p2f1_gn_195201-195212.nc
    │           │           │       │           ├── ...
    │           │           │       │           └── siconc_SImon_EC-Earth3P-HR_hist-1950_r1i1p2f1_gn_201401-201412.nc
    │           │           │       ├── sithick
    │           │           │       │   └── gn
    │           │           │       │       └── v20181212
    │           │           │       │           ├── sithick_SImon_EC-Earth3P-HR_hist-1950_r1i1p2f1_gn_195001-195012.nc
    │           │           │       │           ├── ...
    │           │           │       │           └── sithick_SImon_EC-Earth3P-HR_hist-1950_r1i1p2f1_gn_201401-201412.nc
    │           │           │       ├── siu
    │           │           │       │   └── gn
    │           │           │       │       └── v20181212
    │           │           │       │           ├── siu_SImon_EC-Earth3P-HR_hist-1950_r1i1p2f1_gn_195001-195012.nc
    │           │           │       │           ├── ...
    │           │           │       │           └── siu_SImon_EC-Earth3P-HR_hist-1950_r1i1p2f1_gn_201401-201412.nc
    │           │           │       └── siv
    │           │           │           └── gn
    │           │           │               └── v20181212
    │           │           │                   ├── siv_SImon_EC-Earth3P-HR_hist-1950_r1i1p2f1_gn_195001-195012.nc
    │           │           │                   ├── ...
    │           │           │                   └── siv_SImon_EC-Earth3P-HR_hist-1950_r1i1p2f1_gn_201401-201412.nc
    │           │           ├── r2i1p2f1
    │           │           │   └── SImon
    │           │           │       ├── ...
    │           │           └── r3i1p2f1
    │           │               └── SImon
    │           │                   ├── ...
    │           ├── MOHC
    │           │   ├── HadGEM3-GC31-HM
    │           │   │   └── ...
    │           │   ├── HadGEM3-GC31-LL
    │           │   │   └── ...
    │           │   └── HadGEM3-GC31-MM
    │           │       └── ...
    │           └── ...

"""

def list_available_models(
    data_dir: str = '/seaicecp_data/bergybits/data',
    project: str = 'CMIP6',
    activity_id: str = 'HighResMIP',
    institution_id: (str, [str]) = None,
):
    """ List the names of the models available alphabetically.

        Search the data directory that has been populated by `esgpull` and return a list of all the available models, or `source_id`'s.
        This assumes the `esgpull` convention of subdirectories: `data/project/activity_id/institution_id/source_id`.

        Parameters
        ----------
        data_dir : `str`, optional
            The absolute file path to the data directory.
            The `esgpull` convention means this should end in `/data`.
            Default is `/seaicecp_data/bergybits/data`.
        project : `str`, optional
            The name of the project in which to search for available models.
            Default is `CMIP6`.
        activity_id : `str`, optional
            The name of the activity ID in which to search for available models.
            Default is `HighResMIP`.
        institution_id : `str`, list of `str`, or `None`, optional
            The name(s) of the institution ID(s) in which to search for available models.
            If `None` is given, all available institutions are included.
            Default is `None`.

        Returns
        -------
        model_names : List of `str`
            A list, sorted alphabetically, of the names of the available models.
        
        Examples
        --------
        >>> from seaicecp.path.find_data import list_available_models 
        >>> list_available_models()
        ['AWI/AWI-CM-1-1-HR', 'AWI/AWI-CM-1-1-LR', 'BCC/BCC-CSM2-HR', 'EC-Earth-Consortium/EC-Earth3P', 'EC-Earth-Consortium/EC-Earth3P-HR', 'MOHC/HadGEM3-GC31-HH', 'MOHC/HadGEM3-GC31-HM', 'MOHC/HadGEM3-GC31-LL', 'MOHC/HadGEM3-GC31-MM', 'NCAR/CESM1-CAM5-SE-HR', 'NCAR/CESM1-CAM5-SE-LR', 'NERC/HadGEM3-GC31-HH', 'NERC/HadGEM3-GC31-HM']
        >>> list_available_models(institution_id = 'EC-Earth-Consortium')
        ['EC-Earth-Consortium/EC-Earth3P', 'EC-Earth-Consortium/EC-Earth3P-HR']
        >>> list_available_models(institution_id = 'MOHC')
        ['MOHC/HadGEM3-GC31-HH', 'MOHC/HadGEM3-GC31-HM', 'MOHC/HadGEM3-GC31-LL', 'MOHC/HadGEM3-GC31-MM']
        >>> list_available_models(institution_id = ['MOHC', 'NERC'])
        ['MOHC/HadGEM3-GC31-HH', 'MOHC/HadGEM3-GC31-HM', 'MOHC/HadGEM3-GC31-LL', 'MOHC/HadGEM3-GC31-MM', 'NERC/HadGEM3-GC31-HH', 'NERC/HadGEM3-GC31-HM']
    """
    # Verify input arguments
    if not isinstance(data_dir, str):
        raise TypeError(f"(list_available_models) `data_dir` must be a string. Got type: {type(data_dir)}")
    if not isinstance(project, str):
        raise TypeError(f"(list_available_models) `project` must be a string. Got type: {type(project)}")
    if not isinstance(activity_id, str):
        raise TypeError(f"(list_available_models) `activity_id` must be a string. Got type: {type(activity_id)}")
    if isinstance(institution_id, type([])):
        for this_institution_id in institution_id:
            if not isinstance(this_institution_id, str):
                raise TypeError(f"(list_available_models) Each `institution_id` must be a string. Got type: {type(this_institution_id)}")
    elif not isinstance(institution_id, (str, type(None))):
        raise TypeError(f"(list_available_models) `institution_id` must be a string or `None`. Got type: {type(institution_id)}")
    # Assemble the full file path
    full_path = f"{data_dir}/{project}/{activity_id}"
    # Verify this full path exists
    full_path = verify_path(full_path)

    # Get the institution ID's 
    if isinstance(institution_id, type(None)):
        institution_ids = next(os.walk(full_path))[1]
    elif isinstance(institution_id, str):
        institution_ids = [institution_id]
    else:
        institution_ids = institution_id

    model_names = []
    # Loop through each institution ID
    for this_institution_id in institution_ids:
        # Verify the institution file path exists
        this_institution_path = verify_path(f"{full_path}/{this_institution_id}")
        # Loop across each model for that institution
        for this_model in next(os.walk(this_institution_path))[1]:
            # Verify the model path
            verify_path(f"{this_institution_path}/{this_model}")
            # Add this model to the list
            model_names.append(f"{this_institution_id}/{this_model}")

    return sorted(model_names)

def list_available_variables(
    source_id: str,
    experiment_id: str = None,
    **kwargs,
):
    """ List the names of the variables available for the specified model.

        Search the data directory that has been populated by `esgpull` and return a list of all the available varibles, or `variable_id`'s for the specified model.
        This assumes the `esgpull` convention of subdirectories: `data/project/activity_id/institution_id/source_id/experiment_id/variant_label/table_id/variable_id`.

        Parameters
        ----------
        source_id : `str`
            The name of the source ID (model) for which to find the variable paths.
        experiment_id : `str` or `None`, optional
            The name of the experiment ID in which to search for available variables.
            If `None` is given, all available experiments are included.
            Default is `None`.
        **kwargs
            Keyword arguments to pass to `get_model_path()`.

        Returns
        -------
        avail_var_dict : `dict`
            A dictionary of experiment ID's whose keys are dictionaries of variant labels whose keys are lists of available variables.
        
        Examples
        --------
        >>> from seaicecp.path.find_data import list_available_variables 
        >>> list_available_variables(source_id = 'HadGEM3-GC31-HM')
        {'MOHC/HadGEM3-GC31-HM': {
            'control-1950': {
                'r1i1p1f1': ['areacello']},
            'highres-future': {
                'r1i1p1f1': ['areacello', 'siu', 'siv', 'sithick', 'siconc', 'siage'],
                'r1i3p1f1': ['siconc', 'siage', 'siv', 'sithick', 'siu']},
            'hist-1950': {
                'r1i1p1f1': ['areacello', 'siage', 'siv', 'siu', 'siconc', 'sithick'],
                'r1i3p1f1': ['siconc', 'sithick', 'siu', 'siage', 'siv']}},
        'NERC/HadGEM3-GC31-HM': {
            'highres-future': {
                'r1i2p1f1': ['siv', 'siu', 'siconc', 'sithick', 'siage']},
            'hist-1950': {
                'r1i2p1f1': ['siconc', 'siu', 'sithick', 'siv', 'siage']}}}
        >>> list_available_variables(source_id = 'HadGEM3-GC31-HM', experiment_id = 'hist-1950')
        {'MOHC/HadGEM3-GC31-HM': {
            'hist-1950': {
                'r1i1p1f1': ['areacello', 'siage', 'siv', 'siu', 'siconc', 'sithick'],
                'r1i3p1f1': ['siconc', 'sithick', 'siu', 'siage', 'siv']}},
        'NERC/HadGEM3-GC31-HM': {
            'hist-1950': {
                'r1i2p1f1': ['siconc', 'siu', 'sithick', 'siv', 'siage']}}}
    """
    # Verify input arguments
    if not isinstance(source_id, str):
        raise TypeError(f"(list_available_variables) `source_id` must be a string. Got type: {type(source_id)}")
    if not isinstance(experiment_id, (str, type(None))):
        raise TypeError(f"(list_available_variables) `experiment_id` must be a string or `None`. Got type: {type(experiment_id)}")
    
    # Get the path of the model
    model_paths = get_model_path(source_id, **kwargs)
    # Verify this model path exists
    for i in range(len(model_paths)):
        model_paths[i] = verify_path(model_paths[i])

    # Make a dictionary to store resulting available variables
    avail_var_dict = {f"{model_path.split('/')[-2]}/{model_path.split('/')[-1]}": None for model_path in sorted(model_paths)}

    # Loop across the model paths
    for model_path in model_paths:
        short_model_path = f"{model_path.split('/')[-2]}/{model_path.split('/')[-1]}"
        
        # Get the experiment ID's 
        if isinstance(experiment_id, type(None)):
            experiment_ids = next(os.walk(model_path))[1]
        else:
            experiment_ids = [experiment_id]
        
        # Make a dictionary to store resulting available variables
        avail_var_dict[short_model_path] = {experiment_id: None for experiment_id in sorted(experiment_ids)}

        # Get the variant labels (ensemble members) for each experiment ID
        for this_experiment_id in experiment_ids:
            # Verify the experiment ID path exists
            experiment_path = verify_path(f"{model_path}/{this_experiment_id}")
            # Get the variant labels
            variant_labels = next(os.walk(experiment_path))[1]
            # Add the variant labels as a dictionary to the available variable dictionary
            avail_var_dict[short_model_path][this_experiment_id] = {variant_label: [] for variant_label in sorted(variant_labels)}

            # Get the variables available for each variant label
            for variant_label in variant_labels:
                # Verify the variant path exists
                variant_path = verify_path(f"{experiment_path}/{variant_label}")
                # Get the table ID's
                table_ids = next(os.walk(variant_path))[1]
                # Get the variables available for each table ID
                table_paths = []
                for table_id in table_ids:
                    # Verify the table path exists and add it to the list of table paths
                    table_paths.append(verify_path(f"{variant_path}/{table_id}"))
                # Get the variable names using nested iterations to avoid a list of lists
                avail_var_dict[short_model_path][this_experiment_id][variant_label] = [var_name for path in table_paths for var_name in next(os.walk(path))[1]]

    return avail_var_dict

def list_variable_files(
    source_id: str,
    variable_id: str,
    with_modification: str = None,
    **kwargs,
):
    """ Get a list of data files for the specified variable for the specified model.

        Search for all the files for the given model and variable and return them in a list.
        This assumes the `esgpull` convention of subdirectories: `data/project/activity_id/institution_id/source_id/experiment_id/variant_label/table_id/variable_id/gn/version/data_file.nc`.

        Parameters
        ----------
        source_id : `str`
            The name of the source ID (model) for which to get the variable files.
        variable_id : `str`
            The name of the variable ID for which to get the variable files.
        with_modification : `str`, `None`, optional
            The prefix of a modification to the data files to find.
            Ex: `trim_NWP_`.
            If `None`, returns only the original files.
            Default is `None`.
        **kwargs
            Keyword arguments to pass to `get_variable_path()`.

        Returns
        -------
        data_filepaths : List of `str`
            A list, sorted alphabetically, of the filepaths of the variable data files.
        
        Examples
        --------
        >>> from seaicecp.path.find import list_variable_files
        >>> list_variable_files(source_id = 'HadGEM3-GC31-HM', variable_id = 'areacello')
        ['/seaicecp_data/bergybits/data/CMIP6/HighResMIP/MOHC/HadGEM3-GC31-HM/hist-1950/r1i1p1f1/Ofx/areacello/gn/v20190301/areacello_Ofx_HadGEM3-GC31-HM_hist-1950_r1i1p1f1_gn.nc']
        >>> list_variable_files(source_id = 'EC-Earth3P-HR', variable_id = 'siage')
        /workspace/src/seaicecp/path/find_data.py:399: UserWarning: (get_variable_path) More than one file path found: ['/seaicecp_data/bergybits/data/CMIP6/HighResMIP/EC-Earth-Consortium/EC-Earth3P-HR/hist-1950/r1i1p2f1/SImon/siage', '/seaicecp_data/bergybits/data/CMIP6/HighResMIP/EC-Earth-Consortium/EC-Earth3P-HR/hist-1950/r2i1p2f1/SImon/siage', '/seaicecp_data/bergybits/data/CMIP6/HighResMIP/EC-Earth-Consortium/EC-Earth3P-HR/hist-1950/r3i1p2f1/SImon/siage']
        Returning first result in list.
        ['/seaicecp_data/bergybits/data/CMIP6/HighResMIP/EC-Earth-Consortium/EC-Earth3P-HR/hist-1950/r1i1p2f1/SImon/siage/gn/v20181212/siage_SImon_EC-Earth3P-HR_hist-1950_r1i1p2f1_gn_195001-195012.nc',
        ...
        '/seaicecp_data/bergybits/data/CMIP6/HighResMIP/EC-Earth-Consortium/EC-Earth3P-HR/hist-1950/r1i1p2f1/SImon/siage/gn/v20181212/siage_SImon_EC-Earth3P-HR_hist-1950_r1i1p2f1_gn_201401-201412.nc']
    """
    # Verify input arguments
    if not isinstance(source_id, (str, type(None))):
        raise TypeError(f"(list_variable_files) `source_id` must be a string. Got type: {type(source_id)}")
    if not isinstance(variable_id, str):
        raise TypeError(f"(list_variable_files) `variable_id` must be a string. Got type: {type(variable_id)}")
    if isinstance(with_modification, str):
        if not with_modification.endswith("_"):
            # Make sure the modificatin prefix ends with an underscore
            with_modification = f"{with_modification}_"
    elif not isinstance(with_modification, type(None)):
        raise TypeError(f"(list_variable_files) `with_modification` must be a string or `None`. Got type: {type(with_modification)}")

    # Get the path to the variable directory
    variable_path = get_variable_path(
        source_id = source_id,
        variable_id = variable_id,
        **kwargs,
    )

    # Use glob to get a file path list down to the `data_file` depth
    data_filepaths = glob.glob(f"{variable_path}/*/*/*")

    # Filter files based on modification
    if isinstance(with_modification, type(None)):
        # Filter out files with any modification prefixes
        data_filepaths = [item for item in data_filepaths if not 'trim' in item]
    else:
        # Filter to just files with the modification prefix
        data_filepaths = [item for item in data_filepaths if with_modification in item]

    return sorted(data_filepaths)

def select_files_by_time(
    data_filepaths: [str],
    start: (str, int),
    end: (str, int),
    test: bool = False,
):
    """ Filter the list to be only the files in the given date range. 

        From the given list of datafiles, find the ones that are in between the given start and end dates and return those in a list.

        Parameters
        ----------
        data_filepaths : List of `str`
            A list, sorted alphabetically, of the filepaths of the variable data files.
        start : `str`, `int`
            The start date of the time range, either a string in the format `YYYY-MM-DD` or an integer of a year.
        end : `str`, `int`
            The end date of the time range, either a string in the format `YYYY-MM-DD` or an integer of a year.
        test : `bool`, optional
            If `True`, the function skips verifying the `data_filepaths` exist for use in testing.
            Default is `False`.

        Returns
        -------
        data_filepaths : List of `str`
            A list, sorted alphabetically, of the filepaths in the date range.
        
        Examples
        --------
        >>> from seaicecp.path.find import select_files_by_time
        >>> select_files_by_time(source_id = 'HadGEM3-GC31-HM', variable_id = 'areacello')
        ['/seaicecp_data/bergybits/data/CMIP6/HighResMIP/MOHC/HadGEM3-GC31-HM/hist-1950/r1i1p1f1/Ofx/areacello/gn/v20190301/areacello_Ofx_HadGEM3-GC31-HM_hist-1950_r1i1p1f1_gn.nc']
    """
    # Verify input arguments
    if not isinstance(data_filepaths, type([])):
        raise TypeError(f"(select_files_by_time) `data_filepaths` must be a list. Got type: {type(data_filepaths)}")
    else:
        for filepath in data_filepaths:
            if isinstance(filepath, str):
                # Verify this is a valid path
                if test == False:
                    filepath = verify_path(filepath)
                if not filepath.endswith('.nc'):
                    raise ValueError(f"(select_files_by_time) `filepath` must be a `.nc` filepath. Got: {filepath}")
            else:
                raise TypeError(f"(select_files_by_time) `filepath` must be a string. Got type: {type(filepath)}")
    if isinstance(start, str):
        try:
            # Check that the date follows the expected format
            foo = datetime.strptime(start, "%Y-%m-%d")
            # Get just the year from that date
            start = foo.year
        except ValueError as e:
            raise ValueError(f"(select_files_by_time) `start` must be a date in the format `YYYY-MM-DD`. Got: {start}")
    if isinstance(start, int):
        if start < 1950 or start > 3000:
            raise ValueError(f"(select_files_by_time) `start` must be between 1950 and 3000. Got: {start}")
    else:
        raise TypeError(f"(select_files_by_time) `start` must be a string or `int`. Got type: {type(start)}")
    if isinstance(end, str):
        try:
            # Check that the date follows the expected format
            foo = datetime.strptime(end, "%Y-%m-%d")
            # Get just the year from that date
            end = foo.year
        except ValueError as e:
            raise ValueError(f"(select_files_by_time) `end` must be a date in the format `YYYY-MM-DD`. Got: {end}")
    if isinstance(end, int):
        if end < 1950 or end > 3000:
            raise ValueError(f"(select_files_by_time) `end` must be between 1950 and 3000. Got: {end}")
    else:
        raise TypeError(f"(select_files_by_time) `end` must be a string or `int`. Got type: {type(end)}")
    if start > end:
        raise ValueError(f"(select_files_by_time) `start` must be before `end`. Got `start`: {start} and `end`: {end}")
    if not isinstance(test, (type(True))):
        raise TypeError(f"(select_files_by_time) `test` must be a `bool`. Got type: {type(test)}")

    data_filepaths_in_date_range = []
    # Check each file in the list
    for data_file in data_filepaths:
        # Get the year of the datafile, assuming the following naming convention:
        ## `...<experiment_id>_<variant_label>_gn_YYYYMM-YYYYMM.nc`
        file_years = data_file.split('_')[-1]
        start_year = int(file_years[0:4])
        end_year = int(file_years.split('-')[-1][0:4])
        # If the span of this file crosses the specified date range, include it in the list of files
        if start_year >= start and end_year <= end:
            data_filepaths_in_date_range.append(data_file)

    return sorted(data_filepaths_in_date_range)
