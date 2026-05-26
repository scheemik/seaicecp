import xarray as xr 

from seaicecp.verify import verify_path
from seaicecp.dataset.get_variable import get_variable_name

def get_grid_type(
    dataset: (str, xr.DataArray, xr.Dataset),
):
    """ Get the grid type of the dataset.

        Opens the given datasets, checks the dimensions, and determines the type of grid: regular, irregular, or other.

        Parameters
        ----------
        dataset : `str`, `xarray.DataArray`, `xarray.Dataset`
            The dataset for which to determine the grid type.

        Returns
        -------
        grid_type : `str`
            The type of grid that the dataset has which will be `'regular'`, `'irregular'`, or `'other'`.
        
        Examples
        --------
        >>> from seaicecp.dataset.grid_type import get_grid_type
    """
    # Verify input arguments
    if not isinstance(dataset, (str, xr.Dataset, xr.DataArray)):
        raise TypeError(f"(get_grid_type) `dataset` must be a string, `xr.Dataset`, or `xr.DataArray`. Got type: {type(dataset)}")
    if isinstance(dataset, str):
        # Verify this is a valid path
        dataset = verify_path(dataset)
        if not dataset.endswith('.nc'):
            raise TypeError(f"(get_grid_type) `dataset` must be a `.nc` filepath. Got: {dataset}")
        # Open the dataset
        dataset = xr.open_dataset(dataset)
    
    # Get the variable name for this dataset
    variable_id = get_variable_name(dataset)
    
    # Get the names of the dimensions of the dataset
    ## Note: Use `.sizes` instead of `.dims` for consistency across Datasets and DataArrays
    dims = list(dataset.sizes.keys())

    # Determine the type of spatial grid the dataset has
    if 'j' in dims and 'i' in dims:
        return 'irregular'
    elif ('lat' in dims and 'lon' in dims) or ('latitude' in dims and 'longitude' in dims):
        return 'regular'
    else:
        return 'other'

