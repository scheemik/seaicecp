import xarray as xr
import numpy as np

from seaicecp.verify import verify_path

def make_example_dataset(
    save_as: str = None,
    n : int = 10,
    overwrite: bool = True,
):
    """ Create an example dataset for testing.

        Construct a dataset such that it is minimal in size yet contains all notable features of the datasets of HighResMIP data, and save it to a netCDF file.

        Parameters
        ----------
        save_as : `str`, `None`, optional
            The absolute file path to which to save the example dataset.
            Default is `None`, which doesn't save the dataset to a file.
        n : `int`, optional
            The number of values in each dimension.
            Default is `10`.
        overwrite : `bool`, optional
            Whether to overwrite an existing file at the given filepath in `save_as`.
            Default is `True`.

        Returns
        -------
        example_dataset : `xr.Dataset`
            A list, sorted alphabetically, of the names of the available models.
        
        Examples
        --------
        >>> from seaicecp.dataset.example_dataset import make_example_dataset 
        >>> 
    """
    # Verify input arguments
    if isinstance(save_as, str):
        if not save_as.endswith('.nc'):
            raise ValueError(f"(plot_time_series) `save_as` must be a `.nc` save_as. Got: {save_as}")
    elif not isinstance(save_as, (str, type(None))):
        raise TypeError(f"(make_example_dataset) `save_as` must be a string or `None`. Got type: {type(save_as)}")
    if not isinstance(n, int):
        raise TypeError(f"(make_example_dataset) `n` must be an integer. Got type: {type(n)}")
    if not isinstance(overwrite, bool):
        raise TypeError(f"(make_example_dataset) `overwrite` must be `bool`. Got type: {type(overwrite)}")

    # Initialize the dataset
    xr_dataset = xr.Dataset()
    
    # Add dimensions
    j_arr = np.arange(n, dtype=np.float64)
    xr_dataset['j'] = ('j',j_arr)
    i_arr = np.arange(n+1,2*n+1, dtype=np.float64)
    xr_dataset['i'] = ('i',i_arr)

    # Assign longitude and latitude coordinates
    lon_arr = np.reshape([np.arange(2*n+1,3*n+1, dtype=np.float64)]*n, (n,n))
    lat_arr = np.reshape([np.arange(3*n+1,4*n+1, dtype=np.float64)]*n, (n,n)).T
    xr_dataset = xr_dataset.assign_coords(
        {
            'longitude': (['j','i'], lon_arr),
            'latitude': (['j','i'], lat_arr),
        }
    )

    # Add a test variable
    test_var = np.reshape(np.arange(n*n, dtype=np.float64), (n,n))
    xr_dataset['test_var'] = (['j','i'],test_var)

    if not isinstance(save_as, type(None)):
        # Check whether the file exists
        try:
            verify_path(save_as)
            if overwrite == False:
                raise FileExistsError(f"(trim_files) file `{save_as}` exists already. To overwrite this file, set `overwrite` to `True`.")
            else:
                print(f"\tOverwriting file `{save_as}`.")
        except (FileNotFoundError):
            foo = 2

        # Save this dataset to a file
        xr_dataset.to_netcdf(save_as)

        # Verify that file was save correctly
        save_as = verify_path(save_as)

    return xr_dataset