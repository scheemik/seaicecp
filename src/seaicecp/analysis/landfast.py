import numpy as np
import xarray as xr
from cdo import Cdo
cdo = Cdo()
# Set path for temporary files in case of a crash
cdo = Cdo(tempdir='./cdo_tmp/')
cdo.cleanTempDir()

from seaicecp.verify import verify_path
from seaicecp.dataset.get_variable import get_variable_name

def find_packed_ice(
    dataset: (str, [str], xr.DataArray, xr.Dataset),
    packed_threshold = 85, 
    save_as: str = None,
    **kwargs,
):
    """ Calculate where packed ice is from the dataset.

        Verify the dataset contains the `siconc` variable, and adds a variable `sipacked` which is 1 where `siconc` is greater than 85 percent and 0 elsewhere.

        Parameters
        ----------
        dataset : `str`, list of `str`, `xarray.DataArray`, `xarray.Dataset`
            The dataset of which to find the locations of packed ice.
        packed_threshold : `int`, `float`, optional
            The threshold above which to mark packed ice.
            Default is `85`, following Laliberté et al. 2018.
        save_as : `str`, `None`, optional
            The file name to pass to `cdo.fldmean(output=save_as)`.
            Default is `None`, which doesn't save the dataset to a file.
        **kwargs
            Keyword arguments to pass to `cdo.fldmean()`.

        Returns
        -------
        packedice_xr : `xarray.Dataset`
            A dataset where packed ice is marked as `1` and all other values are `0`.
        
        Examples
        --------
        >>> from seaicecp.dataset.example_dataset import make_example_dataset
        >>> dataset = make_example_dataset(n=3, test_var_name='siconc')
        >>> dataset['siconc'].values
        array([[0., 1., 2.],
               [3., 4., 5.],
               [6., 7., 8.]])
        >>> from seaicecp.analysis.landfast import find_packed_ice
        >>> dataset_sipacked = find_packed_ice(dataset, packed_threshold=4)
        >>> dataset_sipacked['sipacked'].values
        array([[0., 0., 0.],
               [0., 0., 1.],
               [1., 1., 1.]])
    """
    # Verify input arguments
    if isinstance(dataset, str):
        # Wrap that string into a list
        dataset = [dataset]
    if isinstance(dataset, (xr.Dataset, xr.DataArray)):
        input_command = dataset
        cdo_command = cdo.fldmean
    elif isinstance(dataset, type([])):
        if len(dataset) < 1:
            raise ValueError(f"(find_packed_ice) `dataset` must have at least one item. Got: {dataset}")
        # Assemble the `cdo` input command
        input_command = "[ -fldmean :"
        for datafile in dataset:
            if not isinstance(datafile, str):
                raise TypeError(f"(find_packed_ice) Each item in `dataset` list must be a string. Got: {type(datafile)}")
            # Verify this is a valid path
            datafile = verify_path(datafile)
            if not datafile.endswith('.nc'):
                raise TypeError(f"(plot_time_series) `datafile` must be a `.nc` filepath. Got: {datafile}")
            input_command = f"{input_command} {datafile}"
        input_command = f"{input_command} ]"
        print(f"(find_packed_ice) `input`: {input_command}")
        cdo_command = cdo.mergetime
    else:
        raise TypeError(f"(find_packed_ice) `dataset` must be a string, `xr.Dataset`, or `xr.DataArray`. Got type: {type(dataset)}")
    if not isinstance(packed_threshold, (int, float)):
        raise TypeError(f"(find_packed_ice) `packed_threshold` must be `int` or `float`. Got type: {type(packed_threshold)}")
    if not isinstance(save_as, (str, type(None))):
        raise TypeError(f"(find_packed_ice) `save_as` must be a string or `None`. Got type: {type(save_as)}")
    elif isinstance(save_as, str) and not '.nc' in save_as:
        raise TypeError(f"(find_packed_ice) `save_as` must be a `.nc` filepath. Got: {save_as}")

    # Verify this dataset contains the `siconc` variable
    var_name = get_variable_name(dataset)
    if isinstance(var_name, str):
        if not var_name == 'siconc':
            raise ValueError(f"(find_packed_ice) `dataset` must contain the variable `siconc`. Available variables: {var_name}")
    elif isinstance(var_name, type([])):
        if not 'siconc' in var_name:
            raise ValueError(f"(find_packed_ice) `dataset` must contain the variable `siconc`. Available variables: {var_name}")
    else:
        raise TypeError(f"(find_packed_ice) `get_variable_name` returned something other than a string or list: {var_name}")
    
    # Information to output
    print(f"(find_packed_ice) `save_as`: {save_as}")

    # Get the minimum possible integer to cover all reasonable values of `siconc`
    numpy_int32_min = np.iinfo(np.int32).min

    # Create a new dataset for `sipacked`, packed ice
    packedice_xr = cdo.setrtoc2(
        numpy_int32_min,        # Minimum of range
        packed_threshold,       # Maximum of range
        0,                      # Value for grid cells outside range
        1,                      # Value for grid cells within range
        input=dataset, 
        returnXDataset='sipacked'
    )

    # Rename `siconc` in the new dataset to `sipacked`
    return packedice_xr.rename_vars({'siconc':'sipacked'})
