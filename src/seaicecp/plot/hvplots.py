import hvplot.xarray
import xarray as xr
import cartopy.crs as crs

def quadmesh_map(
    xr_data: xr.Dataset, 
    **kwargs,
):
    """ Create an `hvplot` quadmesh map.

        Plot a map of the given data using the `hvplot.quadmesh()` function. 

        Parameters
        ----------
        xr_data : `xarray.Dataset`
            The dataset to plot.
        **kwargs
            Keyword arguments to pass to `hvplot.quadmesh()`.

        Returns
        -------
        qm_map_plot : `holoviews.core.overlay.Overlay`
            An overlay object which can be used to construct the plot.
        
        Examples
        --------
        >>> import xarray as xr
        >>> this_plot = hvplots.quadmesh_map(xr.open_dataset("data/areacello_Ofx_EC-Earth3P-HR_highres-future_r2i1p2f1_gn.nc")
        >>> print(type(this_plot))
        <class 'holoviews.core.overlay.Overlay'>
    """
    # Verify input arguments
    if not isinstance(xr_data, (xr.Dataset, xr.DataArray)):
        raise TypeError(f"(quadmesh_plot) `xr_data` must be `xr.Dataset` or `xr.DataArray`. Got type: {type(xr_data)}")

    # Make the plot
    qm_map_plot = xr_data.areacello.hvplot.quadmesh(
        'longitude', 
        'latitude', 
        projection=crs.Orthographic(-90, 77), 
        project=True,
        global_extent=True, 
        cmap='viridis', 
        coastline=True,
    )
    return qm_map_plot

