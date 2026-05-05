from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import holoviews as hv
from seaicecp.verify import verify_path

def html_to_png(
    html_filename: str, 
    png_filename: str = None,
):
    """ Save an `html` `hvplot` as a `png`.

        Load a previously-saved `html` format plot from `hvplot`, launch a headless browser in which to load it, take a screenshot, and save it to a `png` file.

        Parameters
        ----------
        html_filename : `str`
            The file path within the `outputs/` directory to the `html` file of the `hvplot`.
        png_filename : `str`, `None`, optional
            The file path within the `outputs/` directory to which to save the `png` image, or `None`. 

        Returns
        -------
        None
        
        Examples
        --------
        >>> 
    """
    # Verify input arguments
    if not isinstance(html_filename, str):
        raise TypeError(f"(html_to_png) `html_filename` must be a string. Got type: {type(html_filename)}")
    html_filename = verify_path(f"outputs/{html_filename}")
    if '.html' not in html_filename:
        raise ValueError(f"(html_to_png) `html_filename` must be an `html` filepath. Got: {html_filename}")
    if not isinstance(png_filename, (str, type(None))):
        raise TypeError(f"(html_to_png) `png_filename` must be a string or `None`. Got type: {type(png_filename)}")
    if isinstance(png_filename, str):
        if '.png' not in png_filename:
            raise ValueError(f"(html_to_png) `png_filename` must be a `png` filepath. Got: {png_filename}")
        # Prepend to put it in the `outputs/` directory
        png_filename = f"outputs/{png_filename}"
    if isinstance(png_filename, type(None)):
        # Define the new path to be the same as `html_filename`, but with the `.png` extension
        png_filename = html_filename.replace('.html', '.png')

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
    driver.get("file://" + f"/workspace/{html_filename}")
    # Save a screenshot of that plot as a `png`
    driver.save_screenshot(png_filename)
    # Stop the webdriver
    driver.quit()