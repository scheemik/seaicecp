import hvplot.xarray
import xarray as xr
import cartopy.crs as crs

from seaicecp.plot.save_hvplots import save_hvplot

def quadmesh_map(
    xr_data: xr.Dataset,
    var: str, 
    save_as: str = None,
    **kwargs,
):
    """ Create an `hvplot` quadmesh map.

        Plot a map of the given data using the `hvplot.quadmesh()` function. 

        Parameters
        ----------
        xr_data : `xarray.Dataset`
            The dataset to plot.
        var : `str`
            The variable in `xr_data` to plot.
        save_as : `str`, `None`, optional
            The file name to pass to `seaicecp.plot.save_hvplots.save_hvplot()`.
            Default is `None`, which doesn't save the plot to a file.
        **kwargs
            Keyword arguments to pass to `hvplot.quadmesh()` and 

        Returns
        -------
        qm_map_plot : `holoviews.core.overlay.Overlay`
            An overlay object which can be used to construct the plot.
        
        Examples
        --------
        >>> import xarray as xr
        >>> this_plot = hvplots.quadmesh_map(xr.open_dataset("data/areacello_Ofx_EC-Earth3P-HR_highres-future_r2i1p2f1_gn.nc", 'areacello')
        >>> print(type(this_plot))
        <class 'holoviews.core.overlay.Overlay'>
    """
    # Verify input arguments
    if not isinstance(xr_data, (xr.Dataset, xr.DataArray)):
        raise TypeError(f"(quadmesh_map) `xr_data` must be `xr.Dataset` or `xr.DataArray`. Got type: {type(xr_data)}")
    if not isinstance(var, str):
        raise TypeError(f"(quadmesh_map) `var` must be a string. Got type: {type(var)}")
    if var not in xr_data.data_vars:
        raise ValueError(f"(quadmesh_map) Variable '{var}' not found in `xr_data`. Available variables are: {list(xr_data.data_vars)}")
    if not isinstance(save_as, (str, type(None))):
        raise TypeError(f"(quadmesh_map) `save_as` must be a string or `None`. Got type: {type(save_as)}")
    
    print(f"(quadmesh_map) `save_as`: {save_as}")

    # Make the plot
    qm_map_plot = xr_data[var].hvplot.quadmesh(
        'longitude', 
        'latitude', 
        projection=crs.Orthographic(-90, 77), 
        project=True,
        global_extent=True, 
        cmap='viridis', 
        coastline=True,
    )

    # Save the plot, if applicable
    if not isinstance(save_as, type(None)):
        # Save the plot to file
        save_hvplot(qm_map_plot, save_as)

    return qm_map_plot

