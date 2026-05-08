import os

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
    institution_id: str = None,
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
        institution_id : `str` or `None`, optional
            The name of the institution ID in which to search for available models.
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
        ['AWI-CM-1-1-HR', 'AWI-CM-1-1-LR', 'BCC-CSM2-HR', 'CESM1-CAM5-SE-HR', 'CESM1-CAM5-SE-LR', 'EC-Earth3P', 'EC-Earth3P-HR', 'HadGEM3-GC31-HM', 'HadGEM3-GC31-LL', 'HadGEM3-GC31-MM']
        >>> list_available_models(institution_id = 'EC-Earth-Consortium')
        ['EC-Earth3P', 'EC-Earth3P-HR']
    """
    # Verify input arguments
    if not isinstance(data_dir, str):
        raise TypeError(f"(list_available_models) `data_dir` must be a string. Got type: {type(data_dir)}")
    if not isinstance(project, str):
        raise TypeError(f"(list_available_models) `project` must be a string. Got type: {type(project)}")
    if not isinstance(activity_id, str):
        raise TypeError(f"(list_available_models) `activity_id` must be a string. Got type: {type(activity_id)}")
    if not isinstance(institution_id, (str, type(None))):
        raise TypeError(f"(list_available_models) `institution_id` must be a string or `None`. Got type: {type(institution_id)}")
    # Assemble the full file path
    full_path = f"{data_dir}/{project}/{activity_id}"
    # Verify this full path exists
    full_path = verify_path(full_path)

    # Get the institution ID's 
    if isinstance(institution_id, type(None)):
        institution_ids = next(os.walk(full_path))[1]
    else:
        institution_ids = [institution_id]

    # Verify the paths for each institution ID
    institution_paths = []
    for institution_id in institution_ids:
        # Verify the file path exists and add it to the list of institution paths
        institution_paths.append(verify_path(f"{full_path}/{institution_id}"))
    # Get the model names using nested iterations to avoid a list of lists
    model_names = [model_name for path in institution_paths for model_name in next(os.walk(path))[1]]

    return sorted(model_names)

