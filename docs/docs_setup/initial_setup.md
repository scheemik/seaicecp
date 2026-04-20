<a id='top'></a>
# Initial Setup

This page is under construction.

Much of what follows comes from the incredibly helpful guide, [Python Packages](https://py-pkgs.org/welcome).
Link to the {doc}`README <../index>`.

## Contents

- [The `uv` package manager](#uv_manager)
- [Creating a package structure](#pkg_structure)
    - [Using `uv init`](#uv_init)
    - [Setting the default branch](#default_branch)
    - [Using a `cookiecutter` template](#cookiecutter)
    - [Combining `uv` and `cookiecutter` structures](#uv_and_cookiecutter)
- [Version control and GitHub](#version_control)
- [Virtual environment and packages](#venv)
    - [Activating the virtual environment](#venv_activate)
    - [Adding package dependencies](#venv_dependencies)
    - [Adding `esgpull`](#esgpull)
        - [Adding `esgpull` install on an external drive](#esgpull_ext_HD)
    - [Using a Jupyter notebook](#jupyter_notebook)
- [Building the package](#build_pkg)
- [Documentation](#docs)
    - [Building documentation](#build_docs)
    - [Hosting documentation](#host_docs)
    - [Enabling $\LaTeX$ math syntax](#latex_syntax)
    - [Enabling easy DOI links](#doi_links)

---
<a id='uv_manager'></a>
[back to top](#top)

## The `uv` package manager

In [Python Packages Chapter 2](https://py-pkgs.org/02-setup), the suggest using Miniconda to create an environment and the [`poetry`](https://python-poetry.org/) package to manage dependencies. 
For this project, I decided to use [`uv`](https://docs.astral.sh/uv/) instead. 
From the instructions for [Installing `uv`](https://docs.astral.sh/uv/getting-started/installation/), I used Homebrew.
I've truncated the output below for brevity. 
```console
$ brew install uv
==> Auto-updating Homebrew...
Adjust how often this is run with `$HOMEBREW_AUTO_UPDATE_SECS` or disable with
`$HOMEBREW_NO_AUTO_UPDATE=1`. Hide these hints with `$HOMEBREW_NO_ENV_HINTS=1` (see `man brew`).
==> Downloading https://ghcr.io/v2/homebrew/core/portable-ruby/blobs/sha256:7c7830166a509857669c544dcba7a0d08ca656a3da073c68826ca0a5b1b56b12
################################################################################################################ 100.0%
==> Pouring portable-ruby-4.0.2_1.catalina.bottle.tar.gz
==> Auto-updated Homebrew!
Updated 2 taps (homebrew/core and homebrew/cask).
...
==> Summary
🍺  /usr/local/Cellar/uv/0.11.6: 17 files, 54.0MB
```

I then ensured that I had the most up-to-date version of `uv` installed.
```console
$ brew upgrade uv
Warning: uv 0.11.6 already installed
```


---
<a id='pkg_structure'></a>
[back to top](#top)

## Creating a package structure

<a id='uv_init'></a>
[back to top](#top)

### Using `uv init`

To start a project, I simply need to use `uv` to initiate one, following the [Working on projects](https://docs.astral.sh/uv/guides/projects/) guide.
```console
$ uv init seaicecp --package
Initialized project `seaicecp` at `/<absolute/path/to/project>/seaicecp`
```

This creates a very simple directory structure for the project.
```console
$ tree seaicecp
├── .gitignore
├── .python-version
├── README.md
├── main.py
└── pyproject.toml
```

<a id='default_branch'></a>
[back to top](#top)

### Setting the default branch

For the version of `git` I have, it still sets the default branch as `master`. 
I'm following the guide from Geeks for Geeks on [How to Change Git Default Branch From Master?](https://www.geeksforgeeks.org/git/how-to-change-git-default-branch-from-master/).

First, I renamed the local branch.
```console
Grey@Audron:seaicecp$ git branch -m master main
Grey@Audron:seaicecp$ git push -u origin main
Total 0 (delta 0), reused 0 (delta 0)
remote: 
remote: Create a pull request for 'main' on GitHub by visiting:
remote:      https://github.com/scheemik/seaicecp/pull/new/main
remote: 
To https://github.com/scheemik/seaicecp.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

Then, on GitHub, I went to the "Settings" tab for the repository, then confirmed I was in the "General" section on the sidebar.
Under the heading "Default branch," I clicked the button to "Switch to another branch," selected `main`, then hit "Update."
Next, I deleted the `master` branch from the remote.
```console
Grey@Audron:seaicecp$ git push origin --delete master
To https://github.com/scheemik/seaicecp.git
 - [deleted]         master
```

Since the repository wasn't being used anywhere else, that was all I needed to do.

<a id='cookiecutter'></a>
[back to top](#top)

### Using a `cookiecutter` template

In [Py-Pkgs Section 2.2.2](https://py-pkgs.org/02-setup#install-packaging-software), they suggest installing `cookiecutter` to create a package from a pre-made template. 
This package is then actually used in [Section 3.2.2](https://py-pkgs.org/03-how-to-package-a-python#creating-a-package-structure). 
I do like the package structure they provide with their `cookiecutter` template, but I will need to integrate it with the directory structure generated above with `uv init` as their template assumes using `poetry` as a dependency manager.

With `uv` comes the ability to [invoke a tool without installing it by using `uvx`](https://docs.astral.sh/uv/guides/tools/#running-tools). 
This is helpful when trying something out, or using a tool that is just for set up, like [`cookiecutter`](https://github.com/cookiecutter/cookiecutter), a tool for setting up the structure of the package.
By using `uvx`, you don't need to commit to actually installing `cookiecutter` on your system.

First, I went into a temporary directory, then generated the package structure.
This is to ensure I didn't accidentally overwrite the structure I made with `uv init` earlier.
```console
$ uvx cookiecutter https://github.com/py-pkgs/py-pkgs-cookiecutter.git
Installed 21 packages in 137ms
  [1/7] author_name (Monty Python): Mikhail Schee
  [2/7] package_name (mypkg): seaicecp
  [3/7] package_short_description (A package for doing great things!): Investigate sea ice choke points in the Canadian Arctic Archipelago using high-resolution models.
  [4/7] package_version (0.1.0): 
  [5/7] python_version (3.12): 3.14.1
  [6/7] Select open_source_license
    1 - MIT
    2 - Apache License 2.0
    3 - GNU General Public License v3.0
    4 - CC0 v1.0 Universal
    5 - BSD 3-Clause
    6 - Proprietary
    7 - None
    Choose from [1/2/3/4/5/6/7] (1): 
  [7/7] Select include_github_actions
    1 - no
    2 - ci
    3 - ci+cd
    Choose from [1/2/3] (1):
```

This generates a directory with the chosen package name (in this case, `seaicecp`) and fill it with all the boiler-plate files you would expect in a Python Package.
```console
$ tree seaicecp/
seaicecp/
├── CHANGELOG.md
├── CONDUCT.md
├── CONTRIBUTING.md
├── docs
│   ├── changelog.md
│   ├── conduct.md
│   ├── conf.py
│   ├── contributing.md
│   ├── example.ipynb
│   ├── index.md
│   ├── make.bat
│   ├── Makefile
│   └── requirements.txt
├── LICENSE
├── pyproject.toml
├── README.md
├── src
│   └── seaicecp
│       ├── __init__.py
│       └── seaicecp.py
└── tests
    └── test_seaicecp.py

5 directories, 18 files
```

<a id='uv_and_cookiecutter'></a>
[back to top](#top)

### Combining `uv` and `cookiecutter` structures

Below are the files that are shared across both structures I generated and what changes I needed to make.
- The `src/` directory
    - Use the version generated by the `cookiecutter`.
- `.gitignore`
    - Use the version generated by the `cookiecutter` as it is more extensive.
- `README.md`
    - Use the version generated by the `cookiecutter` as the one generated by `uv init` will be blank.
- `pyproject.toml`
    - Use the version generated by `uv init` as a base.
    - Copy in the lines from the `cookiecutter` version that start with:
        - `description`
        - `authors`
        - `license`

The `pyproject.toml` file initially looks like:
```toml
[project]
name = "seaicecp"
version = "0.1.0"
description = "Investigate sea ice choke points in the Canadian Arctic Archipelago using high-resolution models."
authors = [
    { name = "Mikhail Schee", email = "mikhail.schee@alumni.utoronto.ca" }
]
license = "MIT"
readme = "README.md"
requires-python = ">=3.14"
dependencies = [
    
]

[dependency-groups]
dev = [
    "ipykernel>=7.2.0",
]

[project.scripts]
seaicecp = "seaicecp:main"

[build-system]
requires = ["uv_build>=0.9.15,<0.10.0"]
build-backend = "uv_build"
```

After completing those steps, I deleted the redundant instance of my project directory. 

<a id='version_control'></a>
[back to top](#top)

## Version control and GitHub

Following [Py-Pkgs Section 3.3. Put your package under version control](https://py-pkgs.org/03-how-to-package-a-python#put-your-package-under-version-control), I initiated `git` for my new repository.
```console
$ cd seaicecp/
$ git init
Initialized empty Git repository in /<absolute/path/to/project>/seaicecp/.git/
```

I then added and committed the initial structure and pushed to a new [GitHub repository for the project](https://github.com/scheemik/seaicecp).
I am working in VSCodium, which I'd already set up to [connect to my GitHub account](https://github.com/VSCodium/vscodium/blob/master/docs/usage.md#signin-github), so the process was as simple as pressing the "push" button in the GUI.

<a id='venv'></a>
[back to top](#top)

## Virtual environment and packages

<a id='venv_activate'></a>
[back to top](#top)

### Activating the virtual environment

When initializing the project, `uv` automatically creates a virtual environment in `.venv/`.
I can easily activate it by sourcing that directory.
```console
seaicecp$ source .venv/bin/activate
(seaicecp) seaicecp$ 
```

<a id='venv_dependencies'></a>
[back to top](#top)

### Adding package dependencies

Using `uv` to add dependencies works similarly to `poetry` as described in [3.6. Adding dependencies to your package](https://py-pkgs.org/03-how-to-package-a-python). 
See `uv` docs for [The project environment](https://docs.astral.sh/uv/concepts/projects/layout/#the-project-environment). 

```console
Grey@Audron:seaicecp$ uv add geoviews
Using CPython 3.14.1
Creating virtual environment at: .venv
Resolved 47 packages in 1.35s
      Built cartopy==0.25.0
Prepared 44 packages in 36.06s
Installed 44 packages in 488ms
 + bleach==6.3.0
 + bokeh==3.9.0
 + cartopy==0.25.0
 + certifi==2026.2.25
 + charset-normalizer==3.4.7
 + colorcet==3.1.0
 + contourpy==1.3.3
 + cycler==0.12.1
 + fonttools==4.62.1
 + geoviews==1.15.1
 + holoviews==1.22.1
 + idna==3.11
 + jinja2==3.1.6
 + kiwisolver==1.5.0
 + linkify-it-py==2.1.0
 + markdown==3.10.2
 + markdown-it-py==4.0.0
 + markupsafe==3.0.3
 + matplotlib==3.10.8
 + mdit-py-plugins==0.5.0
 + mdurl==0.1.2
 + narwhals==2.19.0
 + numpy==2.4.4
 + packaging==26.0
 + pandas==3.0.2
 + panel==1.8.10
 + param==2.3.3
 + pillow==12.2.0
 + pyparsing==3.3.2
 + pyproj==3.7.2
 + pyshp==3.0.3
 + python-dateutil==2.9.0.post0
 + pyviz-comms==3.0.6
 + pyyaml==6.0.3
 + requests==2.33.1
 + shapely==2.1.2
 + six==1.17.0
 + tornado==6.5.5
 + tqdm==4.67.3
 + typing-extensions==4.15.0
 + uc-micro-py==2.0.0
 + urllib3==2.6.3
 + webencodings==0.5.1
 + xyzservices==2026.3.0
```

In running that command, I got a pop-up in VSCodium asking: "We noticed a new environment has been created. Do you want to select it for the workspace folder?" I clicked "Yes"

I notice from the list above that `xarray` is not installed. I'll go ahead and add that as well.

```console
Grey@Audron:seaicecp$ uv add xarray
Resolved 48 packages in 343ms
Prepared 1 package in 318ms
Installed 1 package in 11ms
 + xarray==2026.4.0
```

```console
Grey@Audron:seaicecp$ source .venv/bin/activate
(seaicecp) Grey@Audron:seaicecp$ uv add netcdf4
Resolved 78 packages in 716ms
Prepared 2 packages in 3.74s
Installed 2 packages in 13ms
 + cftime==1.6.5
 + netcdf4==1.7.4
```

<a id='esgpull'></a>
[back to top](#top)

### Adding `esgpull`

I want to try downloading more datasets to see whether they are all like this. I found the project [esgpull](https://esgf.github.io/esgf-download/quickstart/) which offers a command line interface for searching and downloading, which I think would be nice as searching on the [ESGF Federated Nodes](https://esgf-node.ornl.gov/search) is a bit tedious with the GUI. 

I'll add `esgpull` as a dependency in my project following the [installation guide](https://esgf.github.io/esgf-download/installation/) which has an example using `uv` which is great.

I came back to this later as I noticed that this didn't actually add `esgpull` to the `.toml` file.
Perhaps I should try installing it with simply `uv add esgpull`?
Would that perhaps mess up the installation I already have? Unclear. 
I could try using the flag `--dry-run` and see what would happen.

```console
(seaicecp) Grey@Audron:seaicecp$ uv tool install esgpull
Resolved 43 packages in 184ms
Prepared 1 package in 142ms
Installed 43 packages in 172ms
 + aiofiles==25.1.0
 + aiostream==0.7.1
 + alembic==1.18.4
 + annotated-types==0.7.0
 + anyio==4.13.0
 + attrs==26.1.0
 + cattrs==26.1.0
 + certifi==2026.2.25
 + cffi==2.0.0
 + click==8.3.2
 + click-params==0.5.0
 + cryptography==46.0.7
 + deprecated==1.3.1
 + esgpull==0.9.6
 + greenlet==3.4.0
 + h11==0.16.0
 + httpcore==1.0.9
 + httpx==0.28.1
 + idna==3.11
 + mako==1.3.11
 + markdown-it-py==4.0.0
 + markupsafe==3.0.3
 + mdurl==0.1.2
 + nest-asyncio==1.6.0
 + packaging==26.1
 + platformdirs==4.9.6
 + pycparser==3.0
 + pydantic==2.13.0
 + pydantic-core==2.46.0
 + pydantic-settings==2.13.1
 + pygments==2.20.0
 + pyopenssl==26.0.0
 + pyparsing==3.3.2
 + python-dotenv==1.2.2
 + pyyaml==6.0.3
 + rich==15.0.0
 + setuptools==82.0.1
 + sqlalchemy==2.0.49
 + tomlkit==0.14.0
 + typing-extensions==4.15.0
 + typing-inspection==0.4.2
 + validators==0.22.0
 + wrapt==2.1.2
Installed 1 executable: esgpull
```

Note: I needed to start a new terminal before the following would work:
```console
(seaicecp) Grey@Audron:seaicecp$ esgpull --version
esgpull, version 0.9.6
```

Then, I needed to do the second step of installation to allow it to write data:
```console
(seaicecp) Grey@Audron:seaicecp$ esgpull self install
──────────────────────────────────────────────────── esgpull installation ────────────────────────────────────────────────────
Install location (/Users/Grey/.esgpull): .esgpull
Name (optional): seaicecp
Creating install directory and files at /Users/Grey/Documents/Research/Postdoc_Projects/York_U_sea_ice/seaicecp/.esgpull
Install config added to /Users/Grey/Library/Application Support/esgpull/installs.json
```

I checked the configuration because the "Server error '500 500' for url 'https://esgf-node.ipsl.upmc.fr/..." got me suspicious as to why it was selected a French web domain:
```console
(seaicecp) Grey@Audron:seaicecp$ esgpull config
──────────────── /Users/Grey/Documents/Research/Postdoc_Projects/York_U_sea_ice/seaicecp/.esgpull/config.toml ────────────────
[paths]
data = "/Users/Grey/Documents/Research/Postdoc_Projects/York_U_sea_ice/seaicecp/.esgpull/data"
db = "/Users/Grey/Documents/Research/Postdoc_Projects/York_U_sea_ice/seaicecp/.esgpull/db"
log = "/Users/Grey/Documents/Research/Postdoc_Projects/York_U_sea_ice/seaicecp/.esgpull/log"
tmp = "/Users/Grey/Documents/Research/Postdoc_Projects/York_U_sea_ice/seaicecp/.esgpull/tmp"
plugins = "/Users/Grey/Documents/Research/Postdoc_Projects/York_U_sea_ice/seaicecp/.esgpull/plugins"

[credentials]
filename = "credentials.toml"

[cli]
page_size = 20

[db]
filename = "esgpull.db"

[download]
chunk_size = 67108864
http_timeout = 20
max_concurrent = 5
disable_ssl = false
disable_checksum = false
show_filename = false

[api]
index_node = "esgf-node.ipsl.upmc.fr"
http_timeout = 20
max_concurrent = 5
page_limit = 50
default_query_id = ""
use_custom_distribution_algorithm = false

[api.default_options]
distrib = "true"
latest = "true"
replica = "none"
retracted = "false"

[plugins]
enabled = false
```

So, that was the issue. I changed the index node to be the one recommended for the USA region:

```console
(seaicecp) Grey@Audron:seaicecp$ esgpull config api.index_node esgf-node.ornl.gov/esgf-1-5-bridge
[api]
index_node = "esgf-node.ornl.gov/esgf-1-5-bridge"

👍 New config file created at /Users/Grey/Documents/Research/Postdoc_Projects/York_U_sea_ice/seaicecp/.esgpull/config.toml.
```

Then, I was finally able to search:
```console
(seaicecp) Grey@Audron:seaicecp$ esgpull search
Found 14423347 datasets.
 id │                               dataset                               │ #  │   size    
════╪═════════════════════════════════════════════════════════════════════╪════╪═══════════
  0 │ cmip5.output.CCCma.CanCM4.decadal1967.mon.land.r7i1p1.v20130331     │ 11 │  56.4 MiB 
  1 │ cmip5.output.CCCma.CanCM4.decadal1967.mon.landIce.r5i1p1.v20130331  │  6 │  22.6 MiB 
  2 │ cmip5.output.CCCma.CanCM4.decadal1982.mon.landIce.r2i1p1.v20130331  │  6 │  22.6 MiB 
  3 │ cmip5.output.CCCma.CanCM4.decadal1982.mon.landIce.r7i1p1.v20130331  │  6 │  22.6 MiB 
  4 │ cmip5.output.CCCma.CanCM4.decadal1982.mon.ocean.r5i1p1.v20130331    │ 32 │   6.6 GiB 
  5 │ cmip5.output.CCCma.CanCM4.decadal1983.day.atmos.r4i1p1.v20130331    │ 23 │   2.6 GiB 
  6 │ cmip5.output.CCCma.CanCM4.decadal1983.day.landIce.r8i1p1.v20130331  │  2 │ 228.3 MiB 
  7 │ cmip5.output.CCCma.CanCM4.decadal1983.mon.atmos.r2i1p1.v20130331    │ 47 │   1.1 GiB 
  8 │ cmip5.output.CCCma.CanCM4.decadal1983.mon.land.r5i1p1.v20130331     │ 11 │  56.4 MiB 
  9 │ cmip5.output.CCCma.CanCM4.decadal1983.mon.landIce.r2i1p1.v20130331  │  6 │  22.6 MiB 
 10 │ cmip5.output.CCCma.CanCM4.decadal1983.mon.ocean.r8i1p1.v20130331    │ 32 │   6.6 GiB 
 11 │ cmip5.output.CCCma.CanCM4.decadal1984.day.atmos.r2i1p1.v20130331    │ 23 │   2.6 GiB 
 12 │ cmip5.output.CCCma.CanCM4.decadal1984.day.landIce.r10i1p1.v20130331 │  2 │ 228.3 MiB 
 13 │ cmip5.output.CCCma.CanCM4.decadal1984.day.seaIce.r3i1p1.v20130331   │  4 │ 456.6 MiB 
 14 │ cmip5.output.CCCma.CanCM4.decadal1980.mon.ocean.r7i1p1.v20130331    │ 96 │  19.8 GiB 
 15 │ cmip5.output.CCCma.CanCM4.decadal1980.mon.ocean.r8i1p1.v20130331    │ 96 │  19.8 GiB 
 16 │ cmip5.output.CCCma.CanCM4.decadal1990.day.atmos.r10i2p1.v20130331   │ 23 │   2.6 GiB 
 17 │ cmip5.output.CCCma.CanCM4.decadal1990.day.atmos.r4i1p1.v20130331    │ 23 │   2.6 GiB 
 18 │ cmip5.output.CCCma.CanCM4.decadal1990.day.atmos.r6i1p1.v20130331    │ 23 │   2.6 GiB 
 19 │ cmip5.output.CCCma.CanCM4.decadal1990.day.land.r5i2p1.v20130331     │  3 │ 342.5 MiB
```

[esgpull download guide](https://esgf.github.io/esgf-download/download/)

<a id='esgpull_ext_HD'></a>
[back to top](#top)

#### Adding `esgpull` install on an external drive

The location chosen for the install is where the data files will be stored. 
My computer's internal hard drive is not large enough to store all the data I will be working with.
To avoid filling up my hard drive, I created a separate `esgpull` install on my external disk. 

First, I confirmed the location of the install I had already done.
```console
Grey@Audron:seaicecp$ esgpull self choose
Install locations                                                                                
 *  /Users/Grey/Documents/Research/Postdoc_Projects/York_U_sea_ice/seaicecp/.esgpull  seaicecp
```

I could not figure out how to input absolute file paths when creating a new `esgpull` install, so I first navigated my terminal to the location in which I wanted it to be.
```console
Grey@Audron:seaicecp$ cd /Volumes/BERGY_BITS/seaicecp_data/
```

Then, I created a new install, giving it a memorable name
```console
Grey@Audron:seaicecp_data$ esgpull self install
──────────────────────────────────────────── esgpull installation ────────────────────────────────────────────
Install location (/Users/Grey/.esgpull): .esgpull
Name (optional): bergybits
Creating install directory and files at /Volumes/BERGY_BITS/seaicecp_data/.esgpull
Install config added to /Users/Grey/Library/Application Support/esgpull/installs.json
```

Now, I can navigate back to the home directory and check which install I have chosen currently.
```console
Grey@Audron:seaicecp_data$ cd ~/Documents/Research/Postdoc_Projects/York_U_sea_ice/seaicecp/
Grey@Audron:seaicecp$ esgpull self choose
Install locations                                                                               
    /Users/Grey/Documents/Research/Postdoc_Projects/York_U_sea_ice/seaicecp/.esgpull  seaicecp  
 *  /Volumes/BERGY_BITS/seaicecp_data/.esgpull 
```

I can confirm what data I've downloaded to each install by using the `show` command.
```console
Grey@Audron:seaicecp$ esgpull self choose -n bergybits
Grey@Audron:seaicecp$ esgpull self choose
Install locations                                                                               
    /Users/Grey/Documents/Research/Postdoc_Projects/York_U_sea_ice/seaicecp/.esgpull  seaicecp  
 *  /Volumes/BERGY_BITS/seaicecp_data/.esgpull                                        bergybits 
Grey@Audron:seaicecp$ esgpull show
Grey@Audron:seaicecp$ esgpull self choose -n seaicecp
Grey@Audron:seaicecp$ esgpull self choose
Install locations                                                                               
 *  /Users/Grey/Documents/Research/Postdoc_Projects/York_U_sea_ice/seaicecp/.esgpull  seaicecp  
    /Volumes/BERGY_BITS/seaicecp_data/.esgpull                                        bergybits 
Grey@Audron:seaicecp$ esgpull show
<1a5a3a>
│ added    2026-04-14T23:07:27Z
│ updated  2026-04-14T23:11:11Z
└── distrib:       True               
    latest:        True               
    replica:       None               
    retracted:     False              
    activity_id:   HighResMIP         
    experiment_id: hist-1950          
    project:       CMIP6              
    source_id:     CESM1-CAM5-SE-HR   
    variable_id:   areacello          
    files:         1 / 1              
    datasets:      1 / 1              
    size:          63.1 MiB / 63.1 MiB
<b1c448>
│ added    2026-04-15T14:44:20Z
│ updated  2026-04-15T14:45:09Z
└── distrib:       True                 
    latest:        True                 
    replica:       None                 
    retracted:     False                
    activity_id:   HighResMIP           
    experiment_id: hist-1950            
    project:       CMIP6                
    variable_id:   areacello            
    files:         7 / 7                
    datasets:      7 / 7                
    size:          419.4 MiB / 419.4 MiB
```

I tried a search:
```console
Grey@Audron:seaicecp$ bash esgpull_searches/HRMIP_hist_areacello.sh 
[2026-04-17 13:58:13]  ERROR     root

  + Exception Group Traceback (most recent call last):
  |   File "/Users/Grey/.local/share/uv/tools/esgpull/lib/python3.14/site-packages/esgpull/tui.py", line 191, in logging
  |     yield
  |   File "/Users/Grey/.local/share/uv/tools/esgpull/lib/python3.14/site-packages/esgpull/cli/search.py", line 102, in search
  |     esg.context.probe()
  |     ~~~~~~~~~~~~~~~~~^^
  |   File "/Users/Grey/.local/share/uv/tools/esgpull/lib/python3.14/site-packages/esgpull/context.py", line 815, in probe
  |     _ = self.hits(
  |         Query(),
  |         file=True,
  |         index_node=index_node or self.config.api.index_node,
  |     )
  |   File "/Users/Grey/.local/share/uv/tools/esgpull/lib/python3.14/site-packages/esgpull/context.py", line 667, in hits
  |     return self._sync(self._hits(*results))
  |            ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^
  |   File "/Users/Grey/.local/share/uv/tools/esgpull/lib/python3.14/site-packages/esgpull/context.py", line 642, in _sync
  |     return sync(self._with_client(coro))
  |   File "/Users/Grey/.local/share/uv/tools/esgpull/lib/python3.14/site-packages/esgpull/utils.py", line 17, in sync
  |     result = asyncio.run(coro)
  |   File "/Users/Grey/.local/share/uv/python/cpython-3.14.1-macos-x86_64-none/lib/python3.14/asyncio/runners.py", line 204, in run
  |     return runner.run(main)
  |            ~~~~~~~~~~^^^^^^
  |   File "/Users/Grey/.local/share/uv/python/cpython-3.14.1-macos-x86_64-none/lib/python3.14/asyncio/runners.py", line 127, in run
  |     return self._loop.run_until_complete(task)
  |            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  |   File "/Users/Grey/.local/share/uv/python/cpython-3.14.1-macos-x86_64-none/lib/python3.14/asyncio/base_events.py", line 719, in run_until_complete
  |     return future.result()
  |            ~~~~~~~~~~~~~^^
  |   File "/Users/Grey/.local/share/uv/tools/esgpull/lib/python3.14/site-packages/esgpull/context.py", line 631, in _with_client
  |     return await coro
  |            ^^^^^^^^^^
  |   File "/Users/Grey/.local/share/uv/tools/esgpull/lib/python3.14/site-packages/esgpull/context.py", line 551, in _hits
  |     async for result in self._fetch(*results):
  |     ...<4 lines>...
  |             hits.append(0)
  |   File "/Users/Grey/.local/share/uv/tools/esgpull/lib/python3.14/site-packages/esgpull/context.py", line 547, in _fetch
  |     raise group
  | ExceptionGroup: fetch (1 sub-exception)
  +-+---------------- 1 ----------------
    | Traceback (most recent call last):
    |   File "/Users/Grey/.local/share/uv/tools/esgpull/lib/python3.14/site-packages/esgpull/context.py", line 518, in _fetch_one
    |     resp.raise_for_status()
    |     ~~~~~~~~~~~~~~~~~~~~~^^
    |   File "/Users/Grey/.local/share/uv/tools/esgpull/lib/python3.14/site-packages/httpx/_models.py", line 829, in raise_for_status
    |     raise HTTPStatusError(message, request=request, response=self)
    | httpx.HTTPStatusError: Server error '500 500' for url 'https://esgf-node.ipsl.upmc.fr/esg-search/search?type=File&offset=0&limit=0&format=application%2Fsolr%2Bjson&fields=instance_id&distrib=true&latest=true&retracted=false'
    | For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/500
    +------------------------------------
ExceptionGroup: fetch (1 sub-exception)
See /Volumes/BERGY_BITS/seaicecp_data/.esgpull/log/esgpull-search-2026-04-17_17-58-12.log for error log.
Aborted!
```

I took a look at the config:
```console
Grey@Audron:seaicecp$ esgpull config
─────────────────────────── /Volumes/BERGY_BITS/seaicecp_data/.esgpull/config.toml ───────────────────────────
[paths]
data = "/Volumes/BERGY_BITS/seaicecp_data/.esgpull/data"
db = "/Volumes/BERGY_BITS/seaicecp_data/.esgpull/db"
log = "/Volumes/BERGY_BITS/seaicecp_data/.esgpull/log"
tmp = "/Volumes/BERGY_BITS/seaicecp_data/.esgpull/tmp"
plugins = "/Volumes/BERGY_BITS/seaicecp_data/.esgpull/plugins"

[credentials]
filename = "credentials.toml"

[cli]
page_size = 20

[db]
filename = "esgpull.db"

[download]
chunk_size = 67108864
http_timeout = 20
max_concurrent = 5
disable_ssl = false
disable_checksum = false
show_filename = false

[api]
index_node = "esgf-node.ipsl.upmc.fr"
http_timeout = 20
max_concurrent = 5
page_limit = 50
default_query_id = ""
use_custom_distribution_algorithm = false

[api.default_options]
distrib = "true"
latest = "true"
replica = "none"
retracted = "false"

[plugins]
enabled = false
```

I changed the index node:
```console
Grey@Audron:seaicecp$ esgpull config api.index_node esgf-node.ornl.gov/esgf-1-5-bridge
[api]
index_node = "esgf-node.ornl.gov/esgf-1-5-bridge"

👍 New config file created at /Volumes/BERGY_BITS/seaicecp_data/.esgpull/config.toml.
```

I confirmed the config changed.
```console
Grey@Audron:seaicecp$ esgpull config
─────────────────────────── /Volumes/BERGY_BITS/seaicecp_data/.esgpull/config.toml ───────────────────────────
[paths]
data = "/Volumes/BERGY_BITS/seaicecp_data/.esgpull/data"
db = "/Volumes/BERGY_BITS/seaicecp_data/.esgpull/db"
log = "/Volumes/BERGY_BITS/seaicecp_data/.esgpull/log"
tmp = "/Volumes/BERGY_BITS/seaicecp_data/.esgpull/tmp"
plugins = "/Volumes/BERGY_BITS/seaicecp_data/.esgpull/plugins"

[credentials]
filename = "credentials.toml"

[cli]
page_size = 20

[db]
filename = "esgpull.db"

[download]
chunk_size = 67108864
http_timeout = 20
max_concurrent = 5
disable_ssl = false
disable_checksum = false
show_filename = false

[api]
index_node = "esgf-node.ornl.gov/esgf-1-5-bridge"
http_timeout = 20
max_concurrent = 5
page_limit = 50
default_query_id = ""
use_custom_distribution_algorithm = false

[api.default_options]
distrib = "true"
latest = "true"
replica = "none"
retracted = "false"

[plugins]
enabled = false
```

Great, it changed. 
Then I tried a search again.
```console
Grey@Audron:seaicecp$ bash esgpull_searches/HRMIP_hist_areacello.sh 
Found 16 datasets.
 id │                              dataset                               │ # │   size    │     data_node      
════╪════════════════════════════════════════════════════════════════════╪═══╪═══════════╪════════════════════
  0 │ CMIP6.HighResMIP.AWI.AWI-CM-1-1-LR.hist-1950.r1i1p1f2.Ofx.areacel… │ 1 │  23.4 MiB │ eagle.alcf.anl.gov 
  1 │ CMIP6.HighResMIP.MOHC.HadGEM3-GC31-HM.hist-1950.r1i1p1f1.Ofx.area… │ 1 │  31.6 MiB │ eagle.alcf.anl.gov 
  2 │ CMIP6.HighResMIP.MOHC.HadGEM3-GC31-MM.hist-1950.r1i1p1f1.Ofx.area… │ 1 │  31.6 MiB │ esgf-node.ornl.gov 
  3 │ CMIP6.HighResMIP.NCAR.CESM1-CAM5-SE-HR.hist-1950.r1i1p1f1.Ofx.are… │ 1 │  63.1 MiB │ eagle.alcf.anl.gov 
  4 │ CMIP6.HighResMIP.AWI.AWI-CM-1-1-HR.hist-1950.r1i1p1f2.Ofx.areacel… │ 1 │ 256.9 MiB │ eagle.alcf.anl.gov 
  5 │ CMIP6.HighResMIP.AWI.AWI-CM-1-1-LR.hist-1950.r1i1p1f2.Ofx.areacel… │ 1 │  23.4 MiB │ esgf-node.ornl.gov 
  6 │ CMIP6.HighResMIP.MOHC.HadGEM3-GC31-HM.hist-1950.r1i1p1f1.Ofx.area… │ 1 │  31.6 MiB │ esgf-node.ornl.gov 
  7 │ CMIP6.HighResMIP.BCC.BCC-CSM2-HR.hist-1950.r1i1p1f1.Ofx.areacello… │ 1 │  11.4 MiB │    cmip.bcc.cma.cn 
  8 │ CMIP6.HighResMIP.NCAR.CESM1-CAM5-SE-HR.hist-1950.r1i1p1f1.Ofx.are… │ 1 │  63.1 MiB │ esgf-node.ornl.gov 
  9 │ CMIP6.HighResMIP.AWI.AWI-CM-1-1-HR.hist-1950.r1i1p1f2.Ofx.areacel… │ 1 │ 256.9 MiB │ esgf-node.ornl.gov 
 10 │ CMIP6.HighResMIP.BCC.BCC-CSM2-HR.hist-1950.r1i1p1f1.Ofx.areacello… │ 1 │  11.4 MiB │ esgf-node.ornl.gov 
 11 │ CMIP6.HighResMIP.BCC.BCC-CSM2-HR.hist-1950.r1i1p1f1.Ofx.areacello… │ 1 │  11.4 MiB │ eagle.alcf.anl.gov 
 12 │ CMIP6.HighResMIP.MOHC.HadGEM3-GC31-LL.hist-1950.r1i1p1f1.Ofx.area… │ 1 │   1.4 MiB │ esgf-node.ornl.gov 
 13 │ CMIP6.HighResMIP.MOHC.HadGEM3-GC31-LL.hist-1950.r1i1p1f1.Ofx.area… │ 1 │   1.4 MiB │ eagle.alcf.anl.gov 
 14 │ CMIP6.HighResMIP.MOHC.HadGEM3-GC31-MM.hist-1950.r1i1p1f1.Ofx.area… │ 1 │  31.6 MiB │ eagle.alcf.anl.gov 
 15 │ CMIP6.HighResMIP.NCAR.CESM1-CAM5-SE-HR.hist-1950.r1i1p1f1.Ofx.are… │ 1 │  63.1 MiB │ esgf-data.ucar.edu
```

<a id='jupyter_notebook'></a>
[back to top](#top)

### Using a Jupyter notebook

I'm now following the `uv` guide on [Using `uv` with Jupyter](https://docs.astral.sh/uv/guides/integration/jupyter/). I'm actually also following the Medium blog post [Create virtual environments with UV to use Jupyter Notebooks inside VS Code](https://medium.com/@luismarcelobp/create-virtual-environments-with-uv-to-use-jupyter-notebooks-inside-vs-code-48f336023e7f).

```console
Grey@Audron:seaicecp$ source .venv/bin/activate
(seaicecp) Grey@Audron:seaicecp$ uv add --dev ipykernel
Resolved 76 packages in 1.08s
Prepared 26 packages in 1.47s
Installed 26 packages in 178ms
 + appnope==0.1.4
 + asttokens==3.0.1
 + comm==0.2.3
 + debugpy==1.8.20
 + decorator==5.2.1
 + executing==2.2.1
 + ipykernel==7.2.0
 + ipython==9.12.0
 + ipython-pygments-lexers==1.1.1
 + jedi==0.19.2
 + jupyter-client==8.8.0
 + jupyter-core==5.9.1
 + matplotlib-inline==0.2.1
 + nest-asyncio==1.6.0
 + parso==0.8.6
 + pexpect==4.9.0
 + platformdirs==4.9.6
 + prompt-toolkit==3.0.52
 + psutil==7.2.2
 + ptyprocess==0.7.0
 + pure-eval==0.2.3
 + pygments==2.20.0
 + pyzmq==27.1.0
 + stack-data==0.6.3
 + traitlets==5.14.3
 + wcwidth==0.6.0
(seaicecp) Grey@Audron:seaicecp$ uv run ipython kernel install --user --env VIRTUAL_ENV $(pwd)/.venv --name=seaicecp_kernel
Installed kernelspec seaicecp_kernel in /Users/Grey/Library/Jupyter/kernels/seaicecp_kernel
```

At this point, I restarted VSCodium. Then, I made a notebook called `testing.ipynb`, then tried to import `xarray`. This brought up a dialogue where I didn't see `seaicecp_kernel`, but I selected ".venv (Python 3.14.1) .venv/bin/python". I then successfully imported `xarray` and `geoviews`. However, I encoutered the following error when I tried to open the dataset:

<a id='build_pkg'></a>
[back to top](#top)

## Building the package

As shown in the [Build systems](https://docs.astral.sh/uv/concepts/projects/config/#build-systems) documentation for `uv`, I used the `--package` flag when initializing the repository. 
In the [Building your package](https://docs.astral.sh/uv/guides/package/#building-your-package) section, I used the 

```console
$ uv sync
Resolved 78 packages in 550ms
      Built seaicecp @ file:///Users/Grey/Documents/Research/Postdoc_Projects/York_U_sea_ice/seaicecp
Prepared 1 package in 53ms
Installed 1 package in 12ms
 + seaicecp==0.1.0 (from file:///Users/Grey/Documents/Research/Postdoc_Projects/York_U_sea_ice/seaicecp)
(seaicecp) Grey@Audron:seaicecp$ uv lock
Resolved 78 packages in 21ms
```

```console
(seaicecp) Grey@Audron:seaicecp$ uv build
Building source distribution (uv build backend)...
Building wheel from source distribution (uv build backend)...
Successfully built dist/seaicecp-0.1.0.tar.gz
Successfully built dist/seaicecp-0.1.0-py3-none-any.whl
```



```console
(seaicecp) Grey@Audron:seaicecp$ uv version
seaicecp 0.1.0
```

I can now import the package in a Jupyter notebook.
```python
import seaicecp 
print(seaicecp.__version__)
```
```console
0.1.0
```

<a id='docs'></a>
[back to top](#top)

## Documentation

<a id='build_docs'></a>
[back to top](#top)

### Building documentation

Adding necessary packages as shown in [3.8.4. Building documentation](https://py-pkgs.org/03-how-to-package-a-python#building-documentation).
```console
Grey@Audron:seaicecp$ source .venv/bin/activate
(seaicecp) Grey@Audron:seaicecp$ uv add --dev myst-nb sphinx-autoapi sphinx-rtd-theme
Resolved 112 packages in 1.08s
      Built seaicecp @ file:///Users/Grey/Documents/Research/Postdoc_Projects/York_U_sea_ice/seaicecp
Prepared 31 packages in 3.20s
Uninstalled 1 package in 8ms
Installed 35 packages in 317ms
 + alabaster==1.0.0
 + astroid==4.1.2
 + attrs==26.1.0
 + babel==2.18.0
 + click==8.3.2
 + docutils==0.22.4
 + fastjsonschema==2.21.2
 + greenlet==3.4.0
 + imagesize==2.0.0
 + importlib-metadata==9.0.0
 + jsonschema==4.26.0
 + jsonschema-specifications==2025.9.1
 + jupyter-cache==1.0.1
 + myst-nb==1.4.0
 + myst-parser==5.0.0
 + nbclient==0.10.4
 + nbformat==5.10.4
 + referencing==0.37.0
 + roman-numerals==4.1.0
 + rpds-py==0.30.0
 ~ seaicecp==0.1.0 (from file:///Users/Grey/Documents/Research/Postdoc_Projects/York_U_sea_ice/seaicecp)
 + snowballstemmer==3.0.1
 + sphinx==9.1.0
 + sphinx-autoapi==3.8.0
 + sphinx-rtd-theme==3.1.0
 + sphinxcontrib-applehelp==2.0.0
 + sphinxcontrib-devhelp==2.0.0
 + sphinxcontrib-htmlhelp==2.1.0
 + sphinxcontrib-jquery==4.1
 + sphinxcontrib-jsmath==1.0.1
 + sphinxcontrib-qthelp==2.0.0
 + sphinxcontrib-serializinghtml==2.0.0
 + sqlalchemy==2.0.49
 + tabulate==0.10.0
 + zipp==3.23.1
```

Then, building the docs. It is necessary to have the environment activated for this step. 
```console
(seaicecp) Grey@Audron:seaicecp$ cd docs
(seaicecp) Grey@Audron:docs$ make html
Running Sphinx v9.1.0
loading translations [en]... done
making output directory... done
myst v5.0.0: MdParserConfig(commonmark_only=False, gfm_only=False, enable_extensions=set(), disable_syntax=[], all_links_external=False, links_external_new_tab=False, url_schemes=('http', 'https', 'mailto', 'ftp'), ref_domains=None, fence_as_directive=set(), number_code_blocks=[], title_to_header=False, heading_anchors=0, heading_slug_func=None, html_meta={}, footnote_sort=True, footnote_transition=True, words_per_minute=200, substitutions={}, linkify_fuzzy_links=True, dmath_allow_labels=True, dmath_allow_space=True, dmath_allow_digits=True, dmath_double_inline=False, update_mathjax=True, mathjax_classes='tex2jax_process|mathjax_process|math|output_area', enable_checkboxes=False, suppress_warnings=[], highlight_code_blocks=True)
myst-nb v1.4.0: NbParserConfig(custom_formats={}, metadata_key='mystnb', cell_metadata_key='mystnb', kernel_rgx_aliases={}, eval_name_regex='^[a-zA-Z_][a-zA-Z0-9_]*$', execution_mode='auto', execution_cache_path='', execution_excludepatterns=(), execution_timeout=30, execution_in_temp=False, execution_allow_errors=False, execution_raise_on_error=False, execution_show_tb=False, merge_streams=False, render_plugin='default', remove_code_source=False, remove_code_outputs=False, scroll_outputs=False, code_prompt_show='Show code cell {type}', code_prompt_hide='Hide code cell {type}', number_source_lines=False, output_stderr='show', render_text_lexer='myst-ansi', render_error_lexer='ipythontb', render_image_options={}, render_figure_options={}, render_markdown_format='commonmark', output_folder='build', append_css=True, metadata_to_fm=False)
Using jupyter-cache at: /Users/Grey/Documents/Research/Postdoc_Projects/York_U_sea_ice/seaicecp/docs/_build/.jupyter_cache
[AutoAPI] Reading files... [ 50%] /Users/Grey/Documents/Research/Postdoc_Projects/York_U_sea_ice/seaicecp/src/
[AutoAPI] Reading files... [100%] /Users/Grey/Documents/Research/Postdoc_Projects/York_U_sea_ice/seaicecp/src/seaicecp/__init__.py
[AutoAPI] Mapping Data... [ 50%] /Users/Grey/Documents/Research/Postdoc_Projects/York_U_sea_ice/seaicecp/src/s
[AutoAPI] Mapping Data... [100%] /Users/Grey/Documents/Research/Postdoc_Projects/York_U_sea_ice/seaicecp/src/seaicecp/__init__.py
[AutoAPI] Rendering Data... [ 50%] seaicecp
[AutoAPI] Rendering Data... [100%] seaicecp.seaicecp

[autosummary] generating autosummary for: changelog.md, conduct.md, contributing.md, example.ipynb, index.md
building [mo]: targets for 0 po files that are out of date
writing output... 
building [html]: targets for 5 source files that are out of date
updating environment: [new config] 8 added, 0 changed, 0 removed
/Users/Grey/Documents/Research/Postdoc_Projects/York_U_sea_ice/seaicecp/docs/example.ipynb: Executing notebook using local CWD [mystnb]
/Users/Grey/Documents/Research/Postdoc_Projects/York_U_sea_ice/seaicecp/docs/example.ipynb: Executed notebook in 1.85 seconds [mystnb]
reading sources... [100%] index
looking for now-outdated files... none found
pickling environment... done
checking consistency... done
preparing documents... done
copying assets... 
copying static files... 
Writing evaluated template result to /Users/Grey/Documents/Research/Postdoc_Projects/York_U_sea_ice/seaicecp/docs/_build/html/_static/basic.css
Writing evaluated template result to /Users/Grey/Documents/Research/Postdoc_Projects/York_U_sea_ice/seaicecp/docs/_build/html/_static/language_data.js
Writing evaluated template result to /Users/Grey/Documents/Research/Postdoc_Projects/York_U_sea_ice/seaicecp/docs/_build/html/_static/documentation_options.js
Writing evaluated template result to /Users/Grey/Documents/Research/Postdoc_Projects/York_U_sea_ice/seaicecp/docs/_build/html/_static/js/versions.js
copying static files: done
copying extra files... 
copying extra files: done
copying assets: done
writing output... [100%] index
generating indices... genindex py-modindex done
highlighting module code... [100%] seaicecp.seaicecp
writing additional pages... search done
dumping search index in English (code: en)... done
dumping object inventory... done
build succeeded.

The HTML pages are in _build/html.
```

Then, I went into the `docs/html/index.html` in VSCodium, hit the preview button, then the top right menu to open the page in a browser.
The test webpage seems like it rendered properly. 

<a id='host_docs'></a>
[back to top](#top)

### Hosting documentation

Following [3.8.5. Hosting documentation online](https://py-pkgs.org/03-how-to-package-a-python#hosting-documentation-online).

First, a few changes need to be made to the `.yaml` file to ensure the documentation can successfully be hosted. 
Upon generating the `cookiecutter` files, the configuration for Read the Docs looked like this:
```yaml
# .readthedocs.yaml
# Read the Docs configuration file
# See https://docs.readthedocs.io/en/stable/config-file/v2.html for details

# Required
version: 2

# Set the OS, Python version and other tools you might need
build:
  os: ubuntu-22.04
  tools:
    python: "3.14.1"
  jobs:
    post_create_environment:
      # Install poetry
      # https://python-poetry.org/docs/#installing-manually
      - pip install poetry
    post_install:
      - VIRTUAL_ENV=$READTHEDOCS_VIRTUALENV_PATH poetry install --all-groups

# Build documentation in the "docs/" directory with Sphinx
sphinx:
  configuration: docs/conf.py
```

Two changes need to be made here. 
The first is to specify the version of Python as `3.14` instead of `3.14.1` as Read the Docs only recognizes up to the minor version number, not the patch number.
Second, the `jobs` section needs to be changed to use `uv` instead of `poetry`.
I followed an example shown in [Issue #11289, Support uv](https://github.com/readthedocs/readthedocs.org/issues/11289) posted on the Read the Docs GitHub page. 
```yaml
# .readthedocs.yaml
# Read the Docs configuration file
# See https://docs.readthedocs.io/en/stable/config-file/v2.html for details

# Required
version: 2

# Set the OS, Python version and other tools you might need
build:
  os: ubuntu-22.04
  tools:
    python: "3.14.1"
  jobs:
    pre_create_environment:
      - asdf plugin add uv
      - asdf install uv latest
      - asdf global uv latest
    create_environment:
      - uv venv $READTHEDOCS_VIRTUALENV_PATH
    install:
      # Use a cache dir in the same mount to halve the install time
      - VIRTUAL_ENV=$READTHEDOCS_VIRTUALENV_PATH uv pip install --cache-dir $READTHEDOCS_VIRTUALENV_PATH/../../uv_cache -r docs/requirements.txt

# Build documentation in the "docs/" directory with Sphinx
sphinx:
  configuration: docs/conf.py

```

Next, I went to [Read the Docs](https://readthedocs.org/) and logged in. 
On the "Projects" dashboard, I clicked "Add project."
On the next page, I selected "Configure manually" then filled in this information:
- Name
    - `seaicecp`
- Repository URL
    - `https://github.com/scheemik/seaicecp`
- Default branch
    - `main`
- Language
    - English

Then, I clicked "Next" and confirmed that the file `.readthedocs.yaml` exists (from using the `cookiecutter` when initializing the repository) and clicked "This file exists."
Upon building, I was greeted with confirmation that the build succeeded. 
```
Version latest / Builds / #32314755 
	git clone --depth 1 https://github.com/scheemik/seaicecp .
	git fetch origin --force --prune --prune-tags --depth 50 refs/heads/main:refs/remotes/origin/main
	git checkout --force origin/main
	cat .readthedocs.yml
	asdf global python 3.14.0
	asdf plugin add uv
	asdf install uv latest
	asdf global uv latest
	uv venv $READTHEDOCS_VIRTUALENV_PATH
	VIRTUAL_ENV=$READTHEDOCS_VIRTUALENV_PATH uv pip install --cache-dir $READTHEDOCS_VIRTUALENV_PATH/../../uv_cache -r docs/requirements.txt
	python -m sphinx -T -j auto -b html -d _build/doctrees -D language=en . $READTHEDOCS_OUTPUT/html
```

Now, the documentation for this project is live and available to view at https://seaicecp.readthedocs.io/en/latest/.
I put that URL in the "About" section of the GitHub repository under "Website."

<a id='latex_syntax'></a>
[back to top](#top)

### Enabling $\LaTeX$ math syntax

In order to be able to use dollar signs to quickly indicate a mathematical symbol from $\LaTeX$, I added the `dollarmath` and `amsmath` extensions to the `docs/conf.py` file's `myst_enable_extensions` list.
```python
myst_enable_extensions = [
    "dollarmath", 
    "amsmath"
]
```

See the MyST-Parser documentation page on [Syntax Extensions](https://myst-parser.readthedocs.io/en/latest/syntax/optional.html)

<a id='doi_links'></a>
[back to top](#top)

### Enabling easy DOI links

Added to `docs/conf.py`:
```python
myst_url_schemes = {
    "http": None,
    "https": None,
    "wiki": "https://en.wikipedia.org/wiki/{{path}}#{{fragment}}",
    "doi": "https://doi.org/{{path}}",
    "gh-issue": {
        "url": "https://github.com/executablebooks/MyST-Parser/issue/{{path}}#{{fragment}}",
        "title": "Issue #{{path}}",
        "classes": ["github"],
    },
}
```

See the MyST-Parser documentation page on [Customizing external URL resolution](https://myst-parser.readthedocs.io/en/latest/syntax/cross-referencing.html#customising-external-url-resolution)