import glob
import os
import warnings

from seaicecp.verify import verify_path
from seaicecp.path.model_paths import get_model_path, list_available_models

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

def get_variable_path(
    source_id: str,
    variable_id: str,
    data_dir: str = '/seaicecp_data/bergybits/data',
    project: str = 'CMIP6',
    activity_id: str = 'HighResMIP',
    experiment_id: str = 'hist-1950',
    variant_label: str = None,
    **kwargs,
):
    """ Find the file path for the specified model and variable.

        Search the data directory that has been populated by `esgpull` for a model's `source_id` and return the file path.
        This assumes the `esgpull` convention of subdirectories: `data/project/activity_id/institution_id/source_id/experiment_id/variant_label/table_id/variable_id`.

        Parameters
        ----------
        source_id : `str`
            The name of the source ID (model) for which to find the variable path.
        variable_id : `str`
            The name of the variable ID for which to find the variable path.
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
        experiment_id : `str`, optional
            The name of the experiment ID in which to search for available variables.
            Default is `hist-1950`.
        variant_label : `str`, `None`, optional
            The name of the variant label (ensemble member) for which to get the variable path.
            If `None` is given, the file path for the first variant with the variable is returned.
            Default is `None`.
        **kwargs
            Keyword arguments to pass to `get_model_path()`.

        Returns
        -------
        variable_path : `str`
            The file path to the directory for the specified variable from the specified model.
        
        Examples
        --------
        >>> from seaicecp.path.find_data import get_variable_path
        >>> get_variable_path(source_id = 'HadGEM3-GC31-HM', variable_id = 'areacello')
        '/seaicecp_data/bergybits/data/CMIP6/HighResMIP/MOHC/HadGEM3-GC31-HM/hist-1950/r1i1p1f1/Ofx/areacello'
        >>> get_variable_path(source_id = 'EC-Earth3P-HR', variable_id = 'siage')
        '/seaicecp_data/bergybits/data/CMIP6/HighResMIP/EC-Earth-Consortium/EC-Earth3P-HR/hist-1950/r3i1p2f1/SImon/siage'
        /workspace/src/seaicecp/path/find_data.py:396: UserWarning: (get_variable_path) More than one file path found: ['/seaicecp_data/bergybits/data/CMIP6/HighResMIP/EC-Earth-Consortium/EC-Earth3P-HR/hist-1950/r1i1p2f1/SImon/siage', '/seaicecp_data/bergybits/data/CMIP6/HighResMIP/EC-Earth-Consortium/EC-Earth3P-HR/hist-1950/r2i1p2f1/SImon/siage', '/seaicecp_data/bergybits/data/CMIP6/HighResMIP/EC-Earth-Consortium/EC-Earth3P-HR/hist-1950/r3i1p2f1/SImon/siage']
        Returning first result in list.
        '/seaicecp_data/bergybits/data/CMIP6/HighResMIP/EC-Earth-Consortium/EC-Earth3P-HR/hist-1950/r1i1p2f1/SImon/siage'
        >>> get_variable_path(source_id = 'EC-Earth3P-HR', variable_id = 'siage', variant_label = 'r3i1p2f1')
        '/seaicecp_data/bergybits/data/CMIP6/HighResMIP/EC-Earth-Consortium/EC-Earth3P-HR/hist-1950/r3i1p2f1/SImon/siage'
    """
    # Verify input arguments
    if not isinstance(source_id, (str, type(None))):
        raise TypeError(f"(get_variable_path) `source_id` must be a string. Got type: {type(source_id)}")
    if not isinstance(variable_id, str):
        raise TypeError(f"(get_variable_path) `variable_id` must be a string. Got type: {type(variable_id)}")
    if not isinstance(data_dir, str):
        raise TypeError(f"(get_variable_path) `data_dir` must be a string. Got type: {type(data_dir)}")
    if not isinstance(project, str):
        raise TypeError(f"(get_variable_path) `project` must be a string. Got type: {type(project)}")
    if not isinstance(activity_id, str):
        raise TypeError(f"(get_variable_path) `activity_id` must be a string. Got type: {type(activity_id)}")
    if not isinstance(experiment_id, str):
        raise TypeError(f"(get_variable_path) `experiment_id` must be a string. Got type: {type(experiment_id)}")
    if not isinstance(variant_label, (str, type(None))):
        raise TypeError(f"(get_variable_path) `variant_label` must be a string or `None`. Got type: {type(variant_label)}")

    # Get the model path
    model_paths = get_model_path(
        source_id = source_id,
        data_dir = data_dir,
        project = project,
        activity_id = activity_id,
    )

    full_variable_id_filepath_list = []

    # Loop across model paths
    for model_path in model_paths:
        # Use glob to get a file path list down to the `variable_id` depth
        variable_id_filepaths = glob.glob(f"{model_path}/*/*/*/*")

        # Filter to just those with the specified variable ID
        variable_id_filepaths = [item for item in variable_id_filepaths if item.endswith(variable_id)]

        # Filter to just those with the specified experiment ID
        variable_id_filepaths = [item for item in variable_id_filepaths if experiment_id in item]

        # Filter to just those with the specified variant label, if applicable
        if not isinstance(variant_label, type(None)):
            variable_id_filepaths = [item for item in variable_id_filepaths if variant_label in item]
        
        # Add this list to the full list
        full_variable_id_filepath_list += variable_id_filepaths

    # Check how many file paths remain
    if len(full_variable_id_filepath_list) > 1:
        # There is more than one matching file path for the specified variable for the specified model
        warnings.warn(f"(get_variable_path) More than one file path found: {sorted(full_variable_id_filepath_list)}\nReturning first result in list.", UserWarning)
        # Return the first variant alphabetically
        return sorted(full_variable_id_filepath_list)[0]
    elif len(full_variable_id_filepath_list) == 0:
        # If no file paths had the variable in it, get the list of available variables and raise an error
        available_variables = list_available_variables(
            source_id = source_id,
            experiment_id = experiment_id,
            data_dir = data_dir,
            project = project,
            activity_id = activity_id,
        )
        raise ValueError(f"(get_variable_path) Variable {variable_id} not found for {source_id}. Available variables: {available_variables}")
    else:
        # If there is only one file path remaining, return it
        return full_variable_id_filepath_list[0]
