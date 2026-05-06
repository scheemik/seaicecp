import xarray as xr

import seaicecp.params as sps

def trim_latlon(
    xr_data: xr.Dataset,
    map_bbox: [float, float, float, float] = sps.NWP_BBOX,
    save_as: str = None,
):
    """ Trim the given dataset.

        Select only the data within the given bounding box of latitude and longitude coordinates from the given dataset.

        Parameters
        ----------
        xr_data : `xarray.Dataset`
            The dataset to plot.
        map_bbox : Array of `float`, optional
            An array of coordinates defining the bounding box of the map in the following format:
                [LAT_MAX, LAT_MIN, LON_MAX, LON_MIN]
            Default is `seaicecp.params.latlon_params.NWP_BBOX`.
        save_as : `str`, `None`, optional
            The file name to pass to `seaicecp.plot.save_hvplots.save_hvplot()`.
            Default is `None`, which doesn't save the plot to a file.

        Returns
        -------
        xr_data_trimmed : `xarray.Dataset`
            The dataset trimmed to the latitude and longitude ranges provided.
        
        Examples
        --------
        >>> 
    """
    # Verify input arguments
    if not isinstance(xr_data, (xr.Dataset, xr.DataArray)):
        raise TypeError(f"(trim_latlon) `xr_data` must be `xr.Dataset` or `xr.DataArray`. Got type: {type(xr_data)}")
    if not isinstance(map_bbox, type([])):
        raise TypeError(f"(trim_latlon) `map_bbox` must be a list. Got type: {type(map_bbox)}")
    elif not len(map_bbox) == 4:
        raise ValueError(f"(trim_latlon) `map_bbox` must have a length of 4. Got length: {len(map_bbox)}")
    else: 
        for i in range(len(map_bbox)):
            if not isinstance(map_bbox[i], (int, float)):
                raise TypeError(f"(trim_latlon) `map_bbox[{i}]` must be a number. Got type: {type(map_bbox[i])}")
    if not isinstance(save_as, (str, type(None))):
        raise TypeError(f"(trim_latlon) `save_as` must be a string or `None`. Got type: {type(save_as)}")
    elif isinstance(save_as, str) and not '.nc' in save_as:
        raise TypeError(f"(trim_latlon) `save_as` must be a `.nc` filepath. Got: {save_as}")
    
    # Information to output
    print(f"(trim_latlon) `save_as`: {save_as}")

    # Unpack the bounding box values
    box_lat_max = map_bbox[0]
    box_lat_min = map_bbox[1]
    box_lon_max = map_bbox[2]
    box_lon_min = map_bbox[3]

    # Check whether the longitude values are negative
    if box_lon_max < 0:
        box_lon_max += 360
    if box_lon_min < 0:
        box_lon_min += 360

    xr_data_trimmed = xr_data.where(
        (xr_data['latitude'] < box_lat_max) &
        (xr_data['latitude'] > box_lat_min) &
        (xr_data['longitude'] > box_lon_min) &
        (xr_data['longitude'] < box_lon_max),
        drop=True,
    )

    # Save the trimmed dataset, if applicable
    if not isinstance(save_as, type(None)):
        # Save the plot to file
        xr_data_trimmed.to_netcdf(save_as)

    return xr_data_trimmed

