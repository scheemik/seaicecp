from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import holoviews as hv

def html_to_png(
    html_filepath: str, 
    png_filepath: str = None,
):
    """ Save an `html` `hvplot` as a `png`.

        Load a previously-saved `html` format plot from `hvplot`, launch a headless browser in which to load it, take a screenshot, and save it to a `png` file.

        Parameters
        ----------
        html_filepath : `str`
            The file path to the `html` file of the `hvplot`.
        png_filepath : `str`, `None`, optional
            The file path to which to save the `png` image, or `None`. 

        Returns
        -------
        None
        
        Examples
        --------
        >>> 
    """
    # Verify input arguments
    if not isinstance(html_filepath, str):
        raise TypeError(f"(html_to_png) `html_filepath` must be a string. Got type: {type(html_filepath)}")
    if not isinstance(png_filepath, (str, type(None))):
        raise TypeError(f"(html_to_png) `png_filepath` must be a string. Got type: {type(png_filepath)}")

    # Activate the `bokeh` extension for HoloViews
    hv.extension("bokeh")

    # Set the options for the webdriver
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Start the chromium webdriver with the above options
    driver = webdriver.Chrome(options=options) 
    # Load the specified `html` plot
    driver.get("file://" + f"/workspace/{html_filepath}")
    # Save a screenshot of that plot as a `png`
    driver.save_screenshot("plot3.png")
    # Stop the webdriver
    driver.quit()